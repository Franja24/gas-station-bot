import unittest
from unittest.mock import Mock, patch

import case_runner


class RunCaseTests(unittest.TestCase):
    @patch("case_runner.generate_pdf_report")
    @patch("case_runner.save_result")
    def test_successful_case_is_passed(self, save_result_mock, report_mock):
        case_function = Mock()

        success = case_runner.run_case("login", case_function)

        self.assertTrue(success)
        case_function.assert_called_once_with()
        result = save_result_mock.call_args.args[0]
        self.assertEqual(result["status"], "PASSED")
        self.assertIsNone(result["error"])
        report_mock.assert_called_once_with(result)

    @patch("case_runner.generate_pdf_report")
    @patch("case_runner.save_result")
    def test_successful_e2e_includes_stage_results(
        self,
        save_result_mock,
        _report_mock,
    ):
        stages = [
            {
                "name": "01_login",
                "status": "PASSED",
                "started_at": "2026-06-05T13:00:00",
                "duration_seconds": 10.0,
                "error": None,
            }
        ]
        case_function = Mock(return_value={"stages": stages})

        success = case_runner.run_case("e2e", case_function)

        self.assertTrue(success)
        result = save_result_mock.call_args.args[0]
        self.assertEqual(result["stages"], stages)

    @patch("case_runner.generate_pdf_report")
    @patch("case_runner.save_result")
    @patch("case_runner.save_screenshot")
    def test_exception_marks_case_as_failed(
        self,
        save_screenshot_mock,
        save_result_mock,
        report_mock,
    ):
        case_function = Mock(side_effect=RuntimeError("screen did not change"))

        success = case_runner.run_case("login", case_function)

        self.assertFalse(success)
        save_screenshot_mock.assert_called_once_with("FAILED_error")
        result = save_result_mock.call_args.args[0]
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(
            result["error"],
            "RuntimeError: screen did not change",
        )
        self.assertIn("RuntimeError: screen did not change", result["traceback"])
        report_mock.assert_called_once_with(result)

    @patch("case_runner.generate_pdf_report")
    @patch("case_runner.save_result")
    @patch(
        "case_runner.save_screenshot",
        side_effect=RuntimeError("screenshot unavailable"),
    )
    def test_screenshot_failure_does_not_hide_original_failure(
        self,
        _save_screenshot_mock,
        save_result_mock,
        _report_mock,
    ):
        case_function = Mock(side_effect=ValueError("original error"))

        success = case_runner.run_case("invoice", case_function)

        self.assertFalse(success)
        result = save_result_mock.call_args.args[0]
        self.assertEqual(result["error"], "ValueError: original error")

    @patch("case_runner.set_screenshot_stage")
    def test_run_stages_records_successful_stages(self, stage_mock):
        login = Mock()
        premium = Mock()

        details = case_runner.run_stages(
            [
                ("01_login", login),
                ("02_premium", premium),
            ]
        )

        login.assert_called_once_with()
        premium.assert_called_once_with()
        self.assertEqual(
            [stage["status"] for stage in details["stages"]],
            ["PASSED", "PASSED"],
        )
        self.assertEqual(
            [stage["name"] for stage in details["stages"]],
            ["01_login", "02_premium"],
        )
        self.assertIn(
            unittest.mock.call("01_login"),
            stage_mock.call_args_list,
        )
        self.assertIn(
            unittest.mock.call("02_premium"),
            stage_mock.call_args_list,
        )

    @patch("case_runner.set_screenshot_stage")
    def test_run_stages_stops_after_failed_stage(self, _stage_mock):
        login = Mock()
        premium = Mock(side_effect=RuntimeError("payment failed"))
        windows = Mock()

        with self.assertRaises(case_runner.StageExecutionError) as context:
            case_runner.run_stages(
                [
                    ("01_login", login),
                    ("02_premium", premium),
                    ("03_windows", windows),
                ]
            )

        windows.assert_not_called()
        self.assertEqual(context.exception.stage_name, "02_premium")
        self.assertEqual(
            [stage["status"] for stage in context.exception.stages],
            ["PASSED", "FAILED"],
        )


if __name__ == "__main__":
    unittest.main()
