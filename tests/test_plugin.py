import copy
from datetime import datetime, timezone, timedelta
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[1]/'plugin'
sys.path.insert(0,str(ROOT/'scripts'))
from common import Invalid, digest
from state import Ledger, summary, schedule_plan
from quotes import compare, COMPONENTS
from extract import extract

T=datetime(2026,10,5,12,tzinfo=timezone.utc)

def intent():
    return dict(product_url='https://books.rakuten.co.jp/rb/12345678/',product_key='synthetic-A',title='Example',seller='Rakuten Books',quantity=1,options={},condition='new',currency='JPY',total='5000',destination='KR',forwarder='malltail',center='JP',recipient_ref='profile-A')

def quotes():
    ctx={'product_key':'A','quantity':1,'destination':'KR','package':{'weight_g':'250','dimensions_cm':['19','14','2'],'basis':'assumed'}}
    rows=[]
    for p in ('malltail','tenso','tensojapan'):
        rows.append({'provider':p,'method':'EMS','context':copy.deepcopy(ctx),'status':'available','source_url':'https://example.com/fees','observed_at':(T-timedelta(hours=1)).isoformat(),'expires_at':(T+timedelta(hours=1)).isoformat(),'components':{k:{'amount':'100','currency':'JPY','basis':'estimated'} for k in COMPONENTS}})
    return {'context':ctx,'quotes':rows}

class StateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.path=Path(self.tmp.name)/'state.sqlite3'; self.l=Ledger(self.path)
        self.r=self.l.create(intent()); self.id=self.r['id']
    def tearDown(self): self.l.close(); self.tmp.cleanup()
    def approve(self, **changes):
        a={'intent_digest':digest(intent()),'max_total':'5100','expires_at':(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat(),'user_evidence_ref':'synthetic-user-message','allow_forwarding':True,'allow_tracking_update':True}; a.update(changes)
        return self.l.approve(self.id,a)
    def resolve(self, r, ref='synthetic-order', outcome='confirmed'):
        return self.l.resolve(self.id,{'attempt_id':r['attempt']['id'],'outcome':outcome,'evidence_ref':'synthetic-evidence','external_ref':ref})
    def order(self):
        self.approve(); return self.resolve(self.l.begin(self.id,'purchase',intent()))
    def test_duplicate_intent_returns_active_run(self):
        new=intent(); new['total']='4000'
        self.assertEqual(self.l.create(new)['id'],self.id)
    def test_order_requires_approval(self):
        with self.assertRaises(Invalid): self.l.begin(self.id,'purchase',intent())
    def test_changed_recipient_and_price_blocked(self):
        self.approve()
        for key,val in [('recipient_ref','profile-B'),('total','5101'),('quantity',2),('options',{'edition':'other'})]:
            data=intent(); data[key]=val
            with self.subTest(key=key),self.assertRaises(Invalid): self.l.begin(self.id,'purchase',data)
    def test_expired_approval_rejected(self):
        with self.assertRaises(Invalid): self.approve(expires_at='2020-01-01T00:00:00Z')
    def test_approval_digest_binding(self):
        with self.assertRaises(Invalid): self.approve(intent_digest='other')
    def test_attempt_survives_reopen_and_unknown(self):
        self.approve(); r=self.l.begin(self.id,'purchase',intent()); self.resolve(r,outcome='unknown')
        l2=Ledger(self.path)
        try:
            with self.assertRaises(Invalid): l2.begin(self.id,'purchase',intent())
            self.assertEqual(l2.read(self.id)['attempt']['status'],'unknown')
        finally:l2.close()
    def test_not_applied_can_retry(self):
        self.approve(); r=self.l.begin(self.id,'purchase',intent()); self.resolve(r,outcome='not_applied')
        self.assertNotEqual(self.l.begin(self.id,'purchase',intent())['attempt']['id'],r['attempt']['id'])
    def test_order_and_forward_cannot_repeat(self):
        self.order()
        with self.assertRaises(Invalid): self.l.begin(self.id,'purchase',intent())
        r=self.l.begin(self.id,'forwarding'); self.resolve(r,'synthetic-forwarding')
        with self.assertRaises(Invalid): self.l.begin(self.id,'forwarding')
    def test_unknown_attempt_cannot_be_cancelled(self):
        self.approve(); self.l.begin(self.id,'purchase',intent())
        with self.assertRaises(Invalid): self.l.cancel(self.id,'cancel-evidence')
    def test_cancel_then_new_run(self):
        self.l.cancel(self.id,'user-cancellation')
        self.assertNotEqual(self.l.create(intent())['id'],self.id)
    def test_event_identity_dedupe_and_reverse_order(self):
        self.order()
        event={'id':'event-A','stage':'warehouse_received','order_ref':'synthetic-order','evidence_ref':'mail-A','occurred_at':'2020-01-01T00:00:00Z','observed_at':'2020-01-01T01:00:00Z'}
        r=self.l.observe(self.id,event); r2=self.l.observe(self.id,event)
        self.assertEqual(len(r['events']),len(r2['events']))
        event.update(id='event-B',stage='seller_shipped')
        self.assertEqual(self.l.observe(self.id,event)['stage'],'warehouse_received')
        event.update(id='event-C',order_ref='old-cancelled-order')
        with self.assertRaises(Invalid):self.l.observe(self.id,event)
    def test_schedule_unique_and_private_summary(self):
        self.order(); self.l.attach_schedule(self.id,'private-schedule')
        with self.assertRaises(Invalid):self.l.attach_schedule(self.id,'duplicate')
        value=json.dumps(summary(self.l.read(self.id)))
        self.assertNotIn('synthetic-order',value); self.assertNotIn('profile-A',value)
        self.assertTrue(schedule_plan(self.l.read(self.id))['requires_first_run_check'])
        self.assertEqual(self.path.stat().st_mode & 0o777,0o600)
    def test_concurrent_purchase_only_one_attempt(self):
        self.approve()
        def worker(_):
            l=Ledger(self.path)
            try:
                l.begin(self.id,'purchase',intent()); return True
            except Invalid:return False
            finally:l.close()
        with ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(worker,range(2)))
        self.assertEqual(sum(results),1)
    def test_check_failure_preserves_last_success(self):
        self.l.record_check(self.id, {'success':True,'observed_at':'2020-01-01T00:00:00Z','evidence_ref':'check-A'})
        r=self.l.record_check(self.id, {'success':False,'observed_at':'2020-01-02T00:00:00Z','evidence_ref':'check-B'})
        self.assertEqual(r['monitor']['last_success_at'],'2020-01-01T00:00:00Z')
        self.assertEqual(r['monitor']['consecutive_failures'],1)
        self.assertIsNone(r['stage'])
    def test_secret_fields_rejected(self):
        data=intent();data['password']='not-a-real-password'
        with self.assertRaises(Invalid):self.l.create(data)

class QuoteTests(unittest.TestCase):
    def test_three_different_services(self):
        d=quotes(); r=compare(d,T)
        self.assertTrue(r['three_valid_providers']); self.assertEqual(r['quotes'][0]['comparable_estimate_jpy'],'600.00')
        d['quotes'][2]['provider']='tenso'
        self.assertFalse(compare(d,T)['three_valid_providers'])
    def test_unknown_not_zero(self):
        d=quotes();d['quotes'][0]['components']['tax']=None
        r=compare(d,T); self.assertIsNone(r['quotes'][0]['comparable_estimate_jpy']);self.assertEqual(r['quotes'][0]['known_cost_jpy'],'500.00')
    def test_stale_mismatched_and_unavailable_not_ranked(self):
        d=quotes();d['quotes'][0]['expires_at']=T.isoformat();d['quotes'][1]['context']['quantity']=2;d['quotes'][2]['status']='unavailable'
        self.assertIsNone(compare(d,T)['lowest_comparable_estimate'])
    def test_fx_direction(self):
        d=quotes();d['fx']={'krw_per_100_jpy':'900','source_url':'https://example.com/fx','basis_date':'2026-10-05','observed_at':(T-timedelta(hours=1)).isoformat(),'expires_at':(T+timedelta(hours=1)).isoformat(),'kind':'synthetic'}
        d['quotes'][0]['components']['goods']={'amount':'9000','currency':'KRW','basis':'quoted'}
        self.assertEqual(compare(d,T)['quotes'][0]['comparable_estimate_jpy'],'1500.00')
        d['fx']['expires_at']=T.isoformat()
        with self.assertRaises(Invalid):compare(d,T)
    def test_nonfinite_and_missing_costs(self):
        for val in ('NaN','Infinity','-1'):
            d=quotes();d['quotes'][0]['components']['goods']['amount']=val
            with self.subTest(val=val),self.assertRaises(Invalid):compare(d,T)
        d=quotes();del d['quotes'][0]['components']['handling']
        with self.assertRaises(Invalid):compare(d,T)

class ParserTests(unittest.TestCase):
    def test_multiple_variants_and_malformed_block(self):
        html=(Path(__file__).parent/'fixtures/product.html').read_text()
        r=extract(html,'https://example.com/product?variant=blue')
        self.assertEqual(len(r['candidates']),2);self.assertEqual(r['parse_failures'],1)
        self.assertTrue(r['requires_visible_page_verification'])
    def test_no_jsonld_is_unknown(self):
        self.assertEqual(extract('<h1>Product</h1>','https://example.com/p')['candidates'],[])
    def test_session_urls_rejected(self):
        with self.assertRaises(Invalid):extract('', 'https://example.com/checkout?token=secret')

class PackageTests(unittest.TestCase):
    def test_manifest_and_all_relative_skill_links(self):
        manifest=json.loads((ROOT/'plugin.json').read_text());self.assertEqual(manifest['name'],'crossborder-purchase')
        import re
        skills=list((ROOT/'skills').glob('*/SKILL.md'));self.assertEqual(len(skills),5)
        for skill in skills:
            for link in re.findall(r'\]\(([^)]+)\)',skill.read_text()):
                self.assertTrue((skill.parent/link).resolve().is_file(),(skill,link))
    def test_cli_dry_run_local_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            file=Path(tmp)/'intent.json';file.write_text(json.dumps(intent()))
            cmd=[sys.executable,str(ROOT/'scripts/purchase_agent.py'),'--state-dir',tmp,'create',str(file)]
            r=json.loads(subprocess.check_output(cmd));self.assertEqual(r['phase'],'draft')
            self.assertFalse(r['has_order']);self.assertIsNone(r['pending_action'])

if __name__=='__main__':unittest.main()
