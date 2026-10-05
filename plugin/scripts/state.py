"""Private transactional ledger. This records evidence, not proof of external success."""
import json
import os
from pathlib import Path
import sqlite3
import uuid
from urllib.parse import urlsplit
from common import fields, require, text, number, instant, now, public_url, digest

INTENT = ('product_url', 'product_key', 'title', 'seller', 'quantity', 'options', 'condition', 'currency', 'total', 'destination', 'forwarder', 'center', 'recipient_ref')
STAGES = ('ordered', 'seller_shipped', 'warehouse_received', 'shipping_quoted', 'shipping_paid', 'international_shipped', 'customs', 'delivered', 'received')


def validate_intent(data):
    fields(data, INTENT, INTENT)
    public_url(data['product_url'])
    for key in ('product_key', 'title', 'seller', 'condition', 'currency', 'destination', 'forwarder', 'center', 'recipient_ref'): text(data[key])
    require(type(data['quantity']) is int and data['quantity'] > 0, 'invalid quantity')
    require(isinstance(data['options'], dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in data['options'].items()), 'invalid options')
    number(data['total'])
    return data


def identity(intent):
    return {k: v for k, v in intent.items() if k != 'total'}


class Ledger:
    def __init__(self, path):
        self.path = Path(path).expanduser().absolute()
        require(not self.path.is_symlink(), 'state file cannot be a symlink')
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        # Create with private permissions before SQLite writes anything.
        fd = os.open(self.path, os.O_CREAT | os.O_RDWR, 0o600); os.close(fd)
        os.chmod(self.path, 0o600)
        self.db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        self.db.execute('PRAGMA journal_mode=DELETE')
        self.db.execute('CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, active INTEGER NOT NULL, data TEXT NOT NULL)')
        self.db.execute('CREATE UNIQUE INDEX IF NOT EXISTS active_intent ON runs(fingerprint) WHERE active=1')

    def close(self): self.db.close()

    def read(self, run_id):
        row = self.db.execute('SELECT data FROM runs WHERE id=?', (run_id,)).fetchone()
        require(row is not None, 'unknown run')
        return json.loads(row[0])

    def create(self, intent):
        validate_intent(intent); fp = digest(identity(intent))
        self.db.execute('BEGIN IMMEDIATE')
        try:
            row = self.db.execute('SELECT data FROM runs WHERE fingerprint=? AND active=1', (fp,)).fetchone()
            if row:
                result = json.loads(row[0]); result['reused'] = True
            else:
                result = {'id': str(uuid.uuid4()), 'intent': intent, 'phase': 'draft', 'stage': None, 'approval': None, 'attempt': None, 'order_ref': None, 'forwarding_ref': None, 'tracking_refs': [], 'automation_ref': None, 'monitor': None, 'events': [], 'created_at': now().isoformat()}
                self.db.execute('INSERT INTO runs VALUES (?,?,1,?)', (result['id'], fp, json.dumps(result, ensure_ascii=False)))
            self.db.execute('COMMIT'); return result
        except Exception:
            self.db.execute('ROLLBACK'); raise

    def change(self, run_id, fn):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            run = self.read(run_id)
            fn(run)
            self.db.execute('UPDATE runs SET data=?, active=? WHERE id=?', (json.dumps(run, ensure_ascii=False), int(run['phase'] not in ('cancelled', 'closed')), run_id))
            self.db.execute('COMMIT'); return run
        except Exception:
            self.db.execute('ROLLBACK'); raise

    def approve(self, run_id, approval):
        fields(approval, ('intent_digest', 'max_total', 'expires_at', 'user_evidence_ref', 'allow_forwarding', 'allow_tracking_update'), ('intent_digest', 'max_total', 'expires_at', 'user_evidence_ref', 'allow_forwarding', 'allow_tracking_update'))
        text(approval['user_evidence_ref']); require(instant(approval['expires_at']) > now(), 'approval expired')
        require(type(approval['allow_forwarding']) is bool and type(approval['allow_tracking_update']) is bool, 'invalid permissions')
        def update(r):
            require(r['phase'] in ('draft', 'approved') and r['attempt'] is None, 'cannot approve this phase')
            require(approval['intent_digest'] == digest(r['intent']), 'approval does not match intent')
            require(number(approval['max_total']) >= number(r['intent']['total']), 'cap below order total')
            r['approval'] = approval; r['phase'] = 'approved'
        return self.change(run_id, update)

    def begin(self, run_id, action, checkout=None):
        require(action in ('purchase', 'forwarding', 'tracking_update'), 'unsupported action')
        def update(r):
            require(r['phase'] not in ('cancelled', 'closed'), 'run is terminal')
            require(r['attempt'] is None, 'unresolved attempt; reconcile first')
            a = r['approval']; require(a is not None, 'human approval missing')
            if action == 'purchase':
                require(instant(a['expires_at']) > now(), 'purchase approval expired')
                require(r['phase'] == 'approved' and r['order_ref'] is None, 'already ordered or not approved')
                validate_intent(checkout)
                require(identity(checkout) == identity(r['intent']), 'checkout conditions changed')
                require(number(checkout['total']) <= number(a['max_total']), 'price exceeds approval')
                require(urlsplit(checkout['product_url']).hostname == 'books.rakuten.co.jp', 'purchase adapter supports Rakuten Books only')
                require(checkout['currency'] == 'JPY' and checkout['destination'] == 'KR' and checkout['forwarder'] == 'malltail' and checkout['center'] == 'JP', 'unsupported execution route')
            elif action == 'forwarding':
                require(a['allow_forwarding'] and r['order_ref'] and not r['forwarding_ref'], 'forwarding not allowed or already registered')
            else:
                require(a['allow_tracking_update'] and r['forwarding_ref'], 'tracking update not authorized')
            r['attempt'] = {'id': str(uuid.uuid4()), 'action': action, 'started_at': now().isoformat(), 'status': 'pending', 'checkout': checkout if action == 'purchase' else None}
        return self.change(run_id, update)

    def resolve(self, run_id, result):
        fields(result, ('attempt_id', 'outcome', 'evidence_ref', 'external_ref'), ('attempt_id', 'outcome', 'evidence_ref'))
        require(result['outcome'] in ('confirmed', 'not_applied', 'unknown'), 'invalid outcome')
        text(result['evidence_ref'])
        def update(r):
            a = r['attempt']; require(a and a['id'] == result['attempt_id'], 'attempt mismatch')
            if result['outcome'] == 'unknown':
                a['status'] = 'unknown'; a['evidence_ref'] = result['evidence_ref']; return
            if result['outcome'] == 'confirmed':
                ref = text(result.get('external_ref'))
                if a['action'] == 'purchase':
                    r['order_ref'] = ref; r['phase'] = 'ordered'; r['stage'] = 'ordered'; r['confirmed_checkout'] = a['checkout']
                elif a['action'] == 'forwarding': r['forwarding_ref'] = ref
                elif ref not in r['tracking_refs']: r['tracking_refs'].append(ref)
            r['events'].append({'id': a['id'], 'type': a['action'] + '_' + result['outcome'], 'evidence_ref': result['evidence_ref'], 'observed_at': now().isoformat()})
            r['attempt'] = None
        return self.change(run_id, update)

    def observe(self, run_id, event):
        fields(event, ('id', 'stage', 'order_ref', 'evidence_ref', 'occurred_at', 'observed_at'), ('id', 'stage', 'order_ref', 'evidence_ref', 'occurred_at', 'observed_at'))
        for key in ('id', 'order_ref', 'evidence_ref'): text(event[key])
        require(event['stage'] in STAGES, 'unknown stage')
        require(instant(event['occurred_at']) <= instant(event['observed_at']) <= now(), 'invalid event time')
        def update(r):
            require(r['phase'] not in ('cancelled', 'closed'), 'run is terminal')
            require(event['order_ref'] == r['order_ref'] and r['order_ref'], 'event belongs to another order')
            if any(e['id'] == event['id'] for e in r['events']): return
            r['events'].append(event)
            if r['stage'] is None or STAGES.index(event['stage']) > STAGES.index(r['stage']): r['stage'] = event['stage']
            if event['stage'] == 'received': r['phase'] = 'closed'
        return self.change(run_id, update)

    def cancel(self, run_id, evidence):
        text(evidence)
        def update(r):
            require(r['attempt'] is None, 'reconcile pending action before cancellation')
            r['phase'] = 'cancelled'
            r['events'].append({'id': str(uuid.uuid4()), 'type': 'cancelled', 'evidence_ref': evidence, 'observed_at': now().isoformat()})
        return self.change(run_id, update)

    def record_check(self, run_id, check):
        fields(check, ('success', 'observed_at', 'evidence_ref'), ('success', 'observed_at', 'evidence_ref'))
        require(type(check['success']) is bool, 'invalid check status')
        require(instant(check['observed_at']) <= now(), 'future check')
        text(check['evidence_ref'])
        def update(r):
            old = r.get('monitor') or {}
            if old:
                require(instant(check['observed_at']) >= instant(old['observed_at']), 'out of order check')
            r['monitor'] = {**check, 'last_success_at': check['observed_at'] if check['success'] else old.get('last_success_at'), 'consecutive_failures': 0 if check['success'] else old.get('consecutive_failures', 0) + 1}
        return self.change(run_id, update)

    def attach_schedule(self, run_id, ref):
        text(ref)
        def update(r):
            require(r['order_ref'] and r['phase'] not in ('cancelled', 'closed'), 'no active order')
            require(r['automation_ref'] in (None, ref), 'schedule exists; update it instead')
            r['automation_ref'] = ref
        return self.change(run_id, update)


def summary(run):
    return {'id': run['id'], 'phase': run['phase'], 'stage': run['stage'], 'intent_digest': digest(run['intent']), 'has_order': bool(run['order_ref']), 'has_forwarding': bool(run['forwarding_ref']), 'tracking_count': len(run['tracking_refs']), 'has_schedule': bool(run['automation_ref']), 'pending_action': None if not run['attempt'] else {'id': run['attempt']['id'], 'action': run['attempt']['action'], 'status': run['attempt']['status']}, 'last_check_at': (run.get('monitor') or {}).get('observed_at'), 'last_success_at': (run.get('monitor') or {}).get('last_success_at'), 'event_count': len(run['events']), 'reused': run.get('reused', False)}


def schedule_plan(run):
    require(run['order_ref'] and run['phase'] not in ('cancelled', 'closed'), 'active order required')
    return {'run_id': run['id'], 'existing_schedule': bool(run['automation_ref']), 'requires_first_run_check': True, 'suggested_frequency': 'daily; ask user for local time', 'prompt': f'Use the crossborder-track-delivery skill to reconcile run {run["id"]} from its configured private state store. Read the linked order emails and seller/forwarder status. Do not purchase, cancel, pay, submit forms, or update tracking automatically. Notify only meaningful changes, access failures or required user actions; unchanged state stays quiet. Stop tracking when cancelled or delivery is confirmed and report whether the schedule was actually stopped. Distinguish carrier delivery from user receipt. Never include private identifiers in notifications.'}
