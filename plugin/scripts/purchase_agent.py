#!/usr/bin/env python3
"""Offline CLI for plugin state, estimates and metadata; no external side effects."""
import argparse
import json
import os
from pathlib import Path
import sys
import sqlite3
from common import Invalid
from quotes import compare
from extract import extract
from state import Ledger, summary, schedule_plan


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--state-dir', default=os.environ.get('PURCHASE_AGENT_STATE_DIR', str(Path.home()/'.local/share/crossborder-purchase')))
    sub = p.add_subparsers(dest='command', required=True)
    for name in ('quote', 'create'):
        sub.add_parser(name).add_argument('input', help='JSON file; never a raw private value')
    ep = sub.add_parser('extract'); ep.add_argument('html'); ep.add_argument('--url', required=True)
    for name in ('status', 'inspect', 'schedule-plan'):
        sub.add_parser(name).add_argument('run_id')
    for name in ('approve', 'resolve', 'observe', 'record-check'):
        sp=sub.add_parser(name); sp.add_argument('run_id'); sp.add_argument('input')
    sp=sub.add_parser('begin'); sp.add_argument('run_id'); sp.add_argument('action', choices=('purchase','forwarding','tracking_update')); sp.add_argument('--input', help='fresh checkout intent for purchase')
    for name in ('cancel', 'attach-schedule'):
        sp=sub.add_parser(name); sp.add_argument('run_id'); sp.add_argument('input', help='JSON object containing evidence_ref or automation_ref')
    args=p.parse_args()
    try:
        data = json.loads(Path(args.input).read_text()) if getattr(args, 'input', None) else None
        if args.command == 'quote': result=compare(data)
        elif args.command == 'extract': result=extract(Path(args.html).read_text(), args.url)
        else:
            ledger=Ledger(Path(args.state_dir)/'ledger.sqlite3')
            try:
                cmd=args.command
                if cmd=='create': result=summary(ledger.create(data))
                elif cmd=='status': result=summary(ledger.read(args.run_id))
                elif cmd=='inspect': result=ledger.read(args.run_id)
                elif cmd=='schedule-plan': result=schedule_plan(ledger.read(args.run_id))
                elif cmd=='approve': result=summary(ledger.approve(args.run_id,data))
                elif cmd=='begin': result=summary(ledger.begin(args.run_id,args.action,data))
                elif cmd=='resolve': result=summary(ledger.resolve(args.run_id,data))
                elif cmd=='observe': result=summary(ledger.observe(args.run_id,data))
                elif cmd=='record-check': result=summary(ledger.record_check(args.run_id,data))
                elif cmd=='cancel': result=summary(ledger.cancel(args.run_id,data['evidence_ref']))
                else: result=summary(ledger.attach_schedule(args.run_id,data['automation_ref']))
            finally: ledger.close()
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (Invalid, ValueError, KeyError, TypeError, OSError, sqlite3.Error) as e:
        # Do not echo untrusted or potentially private input in errors.
        print(json.dumps({'error': str(e) if isinstance(e, Invalid) else 'Invalid input or inaccessible local file'},ensure_ascii=False),file=sys.stderr)
        return 2
    return 0

if __name__=='__main__': raise SystemExit(main())
