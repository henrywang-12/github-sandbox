"""Repeatable correctness scenarios, not a model or performance benchmark."""
import json
import tempfile
from runtime import Runtime


CASES = {
    'success': ('verified', 1),
    'unapproved': ('proposed', 0),
    'expired': ('authorized', 0),
    'revoked': ('authorized', 0),
    'cancelled': ('cancelled', 0),
    'lost_response': ('verified', 1),
    'before_provider': ('indeterminate', 0),
    'after_provider': ('verified', 1),
    'provider_reject': ('failed', 0),
}


def run_scenarios():
    outcomes = []
    for name, (expected_state, expected_bookings) in CASES.items():
        now = [100]
        with tempfile.TemporaryDirectory() as directory:
            with Runtime(directory, clock=lambda: now[0]) as runtime:
                operation = runtime.propose('Example Kitchen', 4)
                if name == 'unapproved':
                    try:
                        runtime.execute(operation)
                    except PermissionError:
                        pass
                elif name == 'cancelled':
                    runtime.cancel(operation)
                else:
                    runtime.approve(operation, runtime.inspect(operation)['request'])
                    if name in ('expired', 'revoked'):
                        if name == 'expired':
                            now[0] = 160
                        else:
                            runtime.revoke(operation)
                        try:
                            runtime.execute(operation)
                        except PermissionError:
                            pass
                    elif name in ('before_provider', 'after_provider', 'provider_reject'):
                        try:
                            runtime.execute(operation, fault=name)
                        except RuntimeError:
                            pass
                    else:
                        runtime.execute(operation, lose_response=name == 'lost_response')
            # Every case is inspected through a newly opened coordinator.
            with Runtime(directory, clock=lambda: now[0]) as runtime:
                if name in ('lost_response', 'before_provider', 'after_provider'):
                    runtime.execute(operation)
                if runtime.inspect(operation)['state'] == 'verified':
                    runtime.execute(operation)  # replay must not duplicate the effect
                    runtime.export_receipt(operation)  # requires matching evidence
                state = runtime.inspect(operation)['state']
                bookings = runtime.booking_count()
                outcomes.append(dict(scenario=name, state=state, bookings=bookings,
                                     passed=state == expected_state and bookings == expected_bookings))
    return dict(schema_version=1, scope='deterministic-local-correctness',
                passed=all(item['passed'] for item in outcomes), scenarios=outcomes)


if __name__ == '__main__':
    report = run_scenarios()
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report['passed'] else 1)
