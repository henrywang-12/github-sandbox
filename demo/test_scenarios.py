import unittest
from scenarios import run_scenarios


class ScenarioTests(unittest.TestCase):
    def test_expected_failure_and_recovery_outcomes_are_reproducible(self):
        report = run_scenarios()
        self.assertTrue(report['passed'], report)
        self.assertEqual(len(report['scenarios']), 9)
        self.assertEqual(report, run_scenarios())
        outcomes = {item['scenario']: item for item in report['scenarios']}
        self.assertEqual(outcomes['before_provider']['state'], 'indeterminate')
        self.assertEqual(outcomes['lost_response']['bookings'], 1)


if __name__ == '__main__':
    unittest.main()
