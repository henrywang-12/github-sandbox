import tempfile
import unittest
from runtime import Runtime


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.now = 100
        self.runtime = Runtime(self.directory.name, clock=lambda: self.now)
        self.operation = self.runtime.propose('Example Kitchen', 4)

    def tearDown(self):
        self.runtime.close()
        self.directory.cleanup()

    def approve(self):
        self.runtime.approve(self.operation, {'restaurant': 'Example Kitchen', 'people': 4})

    def test_unapproved_operation_cannot_write(self):
        with self.assertRaises(PermissionError):
            self.runtime.execute(self.operation)
        self.assertEqual(self.runtime.booking_count(), 0)

    def test_approval_is_bound_to_parameters(self):
        with self.assertRaises(ValueError):
            self.runtime.approve(self.operation, {'restaurant': 'Other', 'people': 4})
        self.assertEqual(self.runtime.inspect(self.operation)['state'], 'proposed')

    def test_expired_approval_cannot_write(self):
        self.approve()
        self.now = 160
        with self.assertRaises(PermissionError):
            self.runtime.execute(self.operation)
        self.assertEqual(self.runtime.booking_count(), 0)

    def test_revoked_approval_cannot_write(self):
        self.approve()
        self.runtime.revoke(self.operation)
        with self.assertRaises(PermissionError):
            self.runtime.execute(self.operation)
        self.assertEqual(self.runtime.booking_count(), 0)

    def test_lost_response_survives_restart_without_duplicate(self):
        self.approve()
        result = self.runtime.execute(self.operation, lose_response=True)
        self.assertEqual(result['state'], 'indeterminate')
        self.assertIsNone(result['receipt'])
        self.runtime.close()
        self.runtime = Runtime(self.directory.name, clock=lambda: self.now)
        # Even an expired/revoked grant allows read-only reconciliation.
        self.now = 200
        self.runtime.revoke(self.operation)
        recovered = self.runtime.execute(self.operation)
        self.assertEqual(recovered['state'], 'verified')
        self.assertTrue(recovered['receipt'].startswith('booking-'))
        for _ in range(5):
            self.runtime.execute(self.operation)
        self.assertEqual(self.runtime.booking_count(), 1)

    def test_missing_provider_evidence_stays_unknown_without_write(self):
        self.approve()
        self.runtime._state(self.operation, 'executing')
        result = self.runtime.execute(self.operation)
        self.assertEqual(result['state'], 'indeterminate')
        self.assertEqual(self.runtime.booking_count(), 0)

    def test_wrong_provider_evidence_cannot_verify(self):
        self.approve()
        self.runtime._state(self.operation, 'executing')
        with self.runtime.provider:
            self.runtime.provider.execute('INSERT INTO bookings VALUES(?,?,?)',
                                          (self.operation, '{}', 'wrong'))
        self.assertEqual(self.runtime.reconcile(self.operation)['state'], 'indeterminate')

    def test_contract_validation(self):
        for people in (True, 0, 13, '4', 1.5):
            with self.subTest(people=people), self.assertRaises(ValueError):
                self.runtime.propose('Example', people)

    def test_second_approval_does_not_extend_grant(self):
        self.approve()
        with self.assertRaises(ValueError):
            self.approve()
        self.assertEqual(self.runtime.inspect(self.operation)['expires'], 160)


if __name__ == '__main__':
    unittest.main()
