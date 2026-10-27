# A durable intent-execution demo

A dependency-free Python experiment accompanying the [position paper](../README.md).
It separates a proposed booking, simulated human approval, provider execution,
and evidence-based verification. Both services are local SQLite databases.
There is no LLM, network access, payment, credential, or real booking.

## Run

Requires Python 3.10 or newer. From the repository root:

```sh
python3 demo/runtime.py --state-dir /tmp/intent-demo-example
python3 -m unittest discover -s demo -v
```

Use a fresh directory to start an empty experiment. Each demo run creates one
new operation. Repeating that *operation* is deduplicated; running the CLI again
is a new operation, not a replay.

## What to observe

1. A typed request proposes four seats at Example Kitchen.
2. Dispatch without approval is blocked and creates no booking.
3. The script simulates a human approving the exact stored request.
4. The provider commits its booking, but the response is deliberately lost.
5. The coordinator records an indeterminate outcome, then restarts.
6. A provider lookup verifies the original booking.
7. Replaying the operation returns that receipt; it creates no duplicate.

The two databases commit independently. This makes the provider/coordinator
failure gap visible without claiming a transaction spanning separate services.

## Experiments

The tests cover changed approval parameters, expired and revoked grants,
missing or mismatched provider evidence, and recovery after restart. They also
verify that repeated execution produces one provider booking.

To explore manually, import `Runtime` from `demo/runtime.py`. Call `propose`,
inspect the returned operation, then pass its exact `request` to `approve`.
`execute(operation, lose_response=True)` injects the lost-response case.

## Boundaries

`Runtime.history(operation)` returns ordered, durable state events. The coordinator
commits each event with its state change. This is an inspection log, not a
tamper-proof audit system; existing databases have no reconstructed history for
events that occurred before this feature was added.

`Runtime.cancel(operation)` permanently cancels an undispatched proposal or
authorized operation. It does not cancel a restaurant booking. Once dispatched,
an operation must be reconciled; cancellation cannot erase an unknown effect.

This is a single-process teaching model, not a production authorization service.
The trusted local caller can approve or revoke operations; no user authentication
is implemented. Anyone with database access can alter records. It assumes no
concurrent callers and has no revocation/dispatch synchronization across workers.
The provider retains deduplication records permanently and supports direct,
authoritative reads; real providers may do neither. A missing record remains
indeterminate rather than triggering an automatic write retry.

There is no general natural-language planner, capability discovery, compensation,
cross-provider orchestration, deployment, or claim of exactly-once distributed
execution. A verified result means this simulated provider stores the matching
booking record, not that a restaurant accepted a reservation in the real world.
