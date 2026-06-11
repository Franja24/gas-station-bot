import unittest
from unittest.mock import patch

from features import sevenly_e2e


class SevenlyE2EFlowTests(unittest.TestCase):
    @patch("features.sevenly_e2e.run_stages")
    def test_runs_sevenly_magna_flow_as_reportable_stages(
        self,
        run_stages_mock,
    ):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = sevenly_e2e.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "01_login",
                "02_sevenly_login",
                "03_magna",
                "04_windows",
                "05_invoice",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                sevenly_e2e.login_run,
                sevenly_e2e.sevenly_login_run,
                sevenly_e2e.magna_run,
                sevenly_e2e.windows_run,
                sevenly_e2e.invoice_run,
            ],
        )


if __name__ == "__main__":
    unittest.main()
