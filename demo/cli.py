"""JSON command interface for the trusted local execution demo."""
import argparse
import json
import sqlite3
import sys
from runtime import Runtime


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', default='.demo-state')
    commands = parser.add_subparsers(dest='command', required=True)
    propose = commands.add_parser('propose')
    propose.add_argument('--restaurant', required=True)
    propose.add_argument('--people', type=int, required=True)
    commands.add_parser('list').add_argument('--limit', type=int, default=20)
    for name in ('inspect', 'history', 'reconcile', 'cancel', 'revoke', 'approve', 'execute', 'receipt'):
        sub = commands.add_parser(name)
        sub.add_argument('operation')
        if name == 'approve':
            sub.add_argument('--request', required=True, help='exact reviewed request as JSON')
            sub.add_argument('--ttl', type=float, default=60)
        if name == 'execute':
            sub.add_argument('--lose-response', action='store_true')
            sub.add_argument('--fault', choices=['before_provider', 'provider_reject', 'after_provider'])
    args = parser.parse_args(argv)
    try:
        with Runtime(args.state_dir) as runtime:
            command = args.command
            if command == 'propose':
                result = runtime.inspect(runtime.propose(args.restaurant, args.people))
            elif command == 'list':
                result = {'operations': runtime.list_operations(args.limit)}
            elif command == 'approve':
                runtime.approve(args.operation, json.loads(args.request), args.ttl)
                result = runtime.inspect(args.operation)
            elif command == 'execute':
                result = runtime.execute(args.operation, args.lose_response, args.fault)
            elif command == 'revoke':
                runtime.revoke(args.operation)
                result = runtime.inspect(args.operation)
            elif command == 'receipt':
                result = runtime.export_receipt(args.operation)
            else:
                result = getattr(runtime, command)(args.operation)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ValueError, KeyError, PermissionError, RuntimeError, sqlite3.Error) as error:
        print(json.dumps({'error': str(error), 'type': type(error).__name__}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
