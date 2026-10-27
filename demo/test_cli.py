import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class CliTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.directory.cleanup()

    def call(self, *arguments, expected=0):
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('cli.py')),
                                 '--state-dir', self.directory.name, *arguments],
                                text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, expected, result.stderr)
        return json.loads(result.stdout if expected == 0 else result.stderr)

    def test_process_separated_approval_and_recovery(self):
        operation = self.call('propose', '--restaurant', 'Example', '--people', '2')['id']
        error = self.call('execute', operation, expected=2)
        self.assertEqual(error['type'], 'PermissionError')
        self.call('approve', operation, '--request', '{"restaurant":"Example","people":2}')
        self.assertEqual(self.call('execute', operation, '--lose-response')['state'], 'indeterminate')
        self.assertEqual(self.call('reconcile', operation)['state'], 'verified')
        self.assertEqual(len(self.call('list')['operations']), 1)
        self.assertEqual(self.call('history', operation)[-1]['kind'], 'verified')

    def test_invalid_requests_and_missing_operation_return_json_errors(self):
        self.assertEqual(self.call('inspect', 'missing', expected=2)['type'], 'KeyError')
        self.assertEqual(self.call('list', '--limit', '0', expected=2)['type'], 'ValueError')
        operation = self.call('propose', '--restaurant', 'Example', '--people', '2')['id']
        self.assertEqual(self.call('approve', operation, '--request', '{', expected=2)['type'],
                         'JSONDecodeError')


if __name__ == '__main__':
    unittest.main()
