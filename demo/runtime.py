"""Local intent execution experiment. No networking, credentials, or real bookings."""
import argparse
import json
import math
import sqlite3
import time
import uuid
from pathlib import Path


class Runtime:
    """Trusted local API; approval here is a simulation, not authentication."""

    def __init__(self, directory, clock=time.time):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        self.clock = clock
        self.db = sqlite3.connect(directory / 'coordinator.sqlite')
        self._closed = False
        try:
            self.provider = sqlite3.connect(directory / 'provider.sqlite')
            for connection in (self.db, self.provider):
                if connection.execute('PRAGMA user_version').fetchone()[0] > 1:
                    raise ValueError('database schema is newer than this demo supports')
        except Exception:
            self.db.close()
            if hasattr(self, 'provider'):
                self.provider.close()
            raise
        self.db.execute('''CREATE TABLE IF NOT EXISTS operations (
            id TEXT PRIMARY KEY, payload TEXT NOT NULL, state TEXT NOT NULL,
            expires REAL, revoked INTEGER NOT NULL DEFAULT 0, receipt TEXT)''')
        self.provider.execute('''CREATE TABLE IF NOT EXISTS bookings (
            operation TEXT PRIMARY KEY, payload TEXT NOT NULL, receipt TEXT NOT NULL)''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS events (
            sequence INTEGER PRIMARY KEY AUTOINCREMENT, operation TEXT NOT NULL,
            kind TEXT NOT NULL, at REAL NOT NULL, detail TEXT NOT NULL)''')
        self.db.commit()
        self.provider.commit()
        for connection in (self.db, self.provider):
            connection.execute('PRAGMA user_version=1')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if not self._closed:
            self.db.close()
            self.provider.close()
            self._closed = True

    def propose(self, restaurant, people):
        if (not isinstance(restaurant, str) or not restaurant.strip()
                or len(restaurant.strip()) > 120
                or any(ord(c) < 32 or ord(c) == 127 for c in restaurant)):
            raise ValueError('restaurant must be 1–120 characters without control characters')
        if type(people) is not int or not 1 <= people <= 12:
            raise ValueError('people must be an integer from 1 to 12')
        operation = str(uuid.uuid4())
        payload = json.dumps({'restaurant': restaurant.strip(), 'people': people},
                             sort_keys=True, separators=(',', ':'))
        with self.db:
            self.db.execute('INSERT INTO operations(id,payload,state) VALUES(?,?,?)',
                            (operation, payload, 'proposed'))
            self._event(operation, 'proposed')
        return operation

    def inspect(self, operation):
        row = self.db.execute('SELECT payload,state,expires,revoked,receipt '
                              'FROM operations WHERE id=?', (operation,)).fetchone()
        if row is None:
            raise KeyError(operation)
        return dict(id=operation, request=json.loads(row[0]), state=row[1],
                    expires=row[2], revoked=bool(row[3]), receipt=row[4])

    def approve(self, operation, reviewed_request, ttl=60):
        """Bind a simulated human decision to the exact stored proposal."""
        if type(ttl) not in (int, float) or not math.isfinite(ttl) or not 0 < ttl <= 3600:
            raise ValueError('ttl must be positive and at most 3600 seconds')
        current = self.inspect(operation)
        if current['state'] != 'proposed':
            raise ValueError('only a new proposal may be approved')
        # Compare canonical encodings: Python equality conflates 1 and True.
        canonical = lambda value: json.dumps(value, sort_keys=True, separators=(',', ':'))
        try:
            reviewed = canonical(reviewed_request)
        except (ValueError, TypeError) as error:
            raise ValueError('reviewed request must be JSON-compatible') from error
        if reviewed != canonical(current['request']):
            raise ValueError('reviewed request differs from proposal')
        with self.db:
            self.db.execute('UPDATE operations SET state=?,expires=? WHERE id=?',
                            ('authorized', self.clock() + ttl, operation))
            self._event(operation, 'authorized', {'expires': self.clock() + ttl})

    def revoke(self, operation):
        self.inspect(operation)
        with self.db:
            self.db.execute('UPDATE operations SET revoked=1 WHERE id=?', (operation,))
            self._event(operation, 'revoked')

    def cancel(self, operation):
        """Cancel only undispatched work; never relabel a completed or unknown effect."""
        current = self.inspect(operation)
        if current['state'] == 'cancelled':
            return current
        if current['state'] not in ('proposed', 'authorized'):
            raise ValueError('dispatched work must be reconciled, not cancelled locally')
        with self.db:
            self.db.execute('UPDATE operations SET state=?,revoked=1 WHERE id=?',
                            ('cancelled', operation))
            self._event(operation, 'cancelled')
        return self.inspect(operation)

    def _event(self, operation, kind, detail=None):
        # Caller owns the transaction, so each state change and event commit together.
        self.db.execute('INSERT INTO events(operation,kind,at,detail) VALUES(?,?,?,?)',
                        (operation, kind, self.clock(), json.dumps(detail or {}, sort_keys=True)))

    def history(self, operation):
        self.inspect(operation)
        return [dict(sequence=row[0], kind=row[1], at=row[2], detail=json.loads(row[3]))
                for row in self.db.execute('SELECT sequence,kind,at,detail FROM events '
                                          'WHERE operation=? ORDER BY sequence', (operation,))]

    def _state(self, operation, state, receipt=None):
        with self.db:
            self.db.execute('UPDATE operations SET state=?,receipt=? WHERE id=?',
                            (state, receipt, operation))
            self._event(operation, state, {'receipt': receipt} if receipt else {})

    def execute(self, operation, lose_response=False, fault=None):
        """Inject local failures: before_provider, provider_reject, after_provider."""
        if fault not in (None, 'before_provider', 'provider_reject', 'after_provider'):
            raise ValueError('unsupported fault injection point')
        current = self.inspect(operation)
        if current['state'] == 'verified':
            return current
        if current['state'] in ('executing', 'indeterminate'):
            # Recovery is read-only. Never blindly redispatch an unknown effect.
            return self.reconcile(operation)
        if current['state'] != 'authorized':
            raise PermissionError('explicit approval is required')
        if current['revoked'] or self.clock() >= current['expires']:
            raise PermissionError('approval expired or was revoked')
        self._state(operation, 'executing')  # durable before provider dispatch
        if fault == 'before_provider':
            raise RuntimeError('simulated crash before provider call')
        if fault == 'provider_reject':
            self._state(operation, 'failed')
            return self.inspect(operation)
        payload = json.dumps(current['request'], sort_keys=True, separators=(',', ':'))
        receipt = 'booking-' + operation
        # The toy provider guarantees permanent deduplication by operation ID.
        # Its separate transaction models an external service commit boundary.
        with self.provider:
            self.provider.execute('INSERT OR IGNORE INTO bookings VALUES(?,?,?)',
                                  (operation, payload, receipt))
            stored = self.provider.execute('SELECT payload FROM bookings WHERE operation=?',
                                           (operation,)).fetchone()[0]
            if stored != payload:
                raise ValueError('operation identity reused with changed parameters')
        if fault == 'after_provider':
            raise RuntimeError('simulated crash after provider commit')
        if lose_response:
            self._state(operation, 'indeterminate')
            return self.inspect(operation)
        return self.reconcile(operation)

    def reconcile(self, operation):
        current = self.inspect(operation)
        if current['state'] not in ('executing', 'indeterminate', 'verified'):
            raise ValueError('only dispatched operations can be reconciled')
        row = self.provider.execute('SELECT payload,receipt FROM bookings WHERE operation=?',
                                    (operation,)).fetchone()
        expected = json.dumps(current['request'], sort_keys=True, separators=(',', ':'))
        if row and row[0] == expected:
            self._state(operation, 'verified', row[1])
        else:
            self._state(operation, 'indeterminate')
        return self.inspect(operation)

    def booking_count(self):
        return self.provider.execute('SELECT count(*) FROM bookings').fetchone()[0]

    def list_operations(self, limit=20):
        if type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError('limit must be an integer from 1 to 100')
        return [self.inspect(row[0]) for row in self.db.execute(
            'SELECT id FROM operations ORDER BY rowid DESC LIMIT ?', (limit,)).fetchall()]

    def export_receipt(self, operation):
        """Export evidence only after checking both coordinator and provider records."""
        current = self.inspect(operation)
        if current['state'] != 'verified':
            raise ValueError('only verified operations have exportable receipts')
        row = self.provider.execute('SELECT payload,receipt FROM bookings WHERE operation=?',
                                    (operation,)).fetchone()
        expected = json.dumps(current['request'], sort_keys=True, separators=(',', ':'))
        if not row or row[0] != expected or row[1] != current['receipt']:
            raise ValueError('provider evidence no longer matches the verified record')
        return dict(schema_version=1, operation=operation, request=current['request'],
                    provider_reference=row[1], evidence_scope='local-simulated-provider-record')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', default='.demo-state')
    args = parser.parse_args()
    runtime = Runtime(args.state_dir)
    operation = runtime.propose('Example Kitchen', 4)
    print('1. Proposed:', runtime.inspect(operation))
    try:
        runtime.execute(operation)
    except PermissionError as error:
        print('2. Blocked before approval:', error)
    runtime.approve(operation, runtime.inspect(operation)['request'])
    print('3. Simulated human approval recorded for this exact request.')
    print('4. Provider commits; response lost:',
          runtime.execute(operation, lose_response=True)['state'])
    runtime.close()
    runtime = Runtime(args.state_dir)
    print('5. Restart and reconcile:', runtime.execute(operation)['state'])
    print('6. Repeat operation:', runtime.execute(operation)['state'])
    receipt = runtime.inspect(operation)['receipt']
    print('7. Verified receipt:', receipt)
    print('8. Bookings for this operation:', runtime.provider.execute(
        'SELECT count(*) FROM bookings WHERE operation=?', (operation,)).fetchone()[0])
    runtime.close()


if __name__ == '__main__':
    main()
