import unittest
from unittest.mock import Mock, patch

import case_runner


class RunCaseTests(unittest.TestCase):
    def setUp(self):
        self.after_run_enabled_patcher = patch(
            "case_runner.is_pos_log_after_run_enabled",
            return_value=False,
        )
        self.copy_pos_log_patcher = patch(
            "case_runner.copy_latest_pos_log_to_run_folder"
        )
        self.after_run_enabled_mock = self.after_run_enabled_patcher.start()
        self.copy_pos_log_mock = self.copy_pos_log_patcher.start()
        self.addCleanup(self.after_run_enabled_patcher.stop)
        self.addCleanup(self.copy_pos_log_patcher.stop)

    @patch("case_runner.generate_pdf_report")
    @patch("case_runner.generate_excel_report")
    @patch("case_runner.save_result")
    def test_successful_case_is_passed(
        self,
        save_result_mock,
        excel_report_mock,
        report_mock,
    ):
        case_function = Mock()

        success = case_runner.run_case("login", case_function)

        self.assertTrue(success)
        case_function.assert_called_once_with()
        result = save_result_mock.call_args.args[0]
        self.assertEqual(result["status"], "PASSED")
        self.assertIsNone(result["error"])
        excel_report_mock.assert_called_once()
        report_mock.assert_called_once_with(result)
        self.copy_pos_log_mock.assert_not_called()

    @patch("case_runner.generate_pdf_report")
    @patch("case_runner.generate_excel_report")
    @patch("case_runner.save_result")
    def test_successful_e2e_includes_stage_results(
        self,
        save_result_mock,
        _excel_report_mock,
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
    @patch("case_runner.generate_excel_report")
    @patch("case_runner.save_result")
    @patch("case_runner.save_screenshot")
    def test_exception_marks_case_as_failed(
        self,
        save_screenshot_mock,
        save_result_mock,
        _excel_report_mock,
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
    @patch("case_runner.generate_excel_report")
    @patch("case_runner.save_result")
    @patch(
        "case_runner.save_screenshot",
        side_effect=RuntimeError("screenshot unavailable"),
    )
    def test_screenshot_failure_does_not_hide_original_failure(
        self,
        _save_screenshot_mock,
        save_result_mock,
        _excel_report_mock,
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

    @patch("case_runner.set_screenshot_stage")
    @patch("case_runner.save_screenshot")
    def test_run_suite_continues_after_failed_case(
        self,
        save_screenshot_mock,
        _stage_mock,
    ):
        first_case = Mock(return_value={"stages": []})
        failed_case = Mock(side_effect=RuntimeError("payment failed"))
        last_case = Mock(return_value={"stages": []})

        details = case_runner.run_suite(
            [
                ("01_first", first_case),
                ("02_failed", failed_case),
                ("03_last", last_case),
            ]
        )

        first_case.assert_called_once_with()
        failed_case.assert_called_once_with()
        last_case.assert_called_once_with()
        save_screenshot_mock.assert_called_once_with("FAILED_error")
        self.assertEqual(details["status"], "FAILED")
        self.assertEqual(
            details["suite_summary"],
            {
                "total": 3,
                "passed": 2,
                "failed": 1,
            },
        )
        self.assertEqual(
            [case["status"] for case in details["suite_cases"]],
            ["PASSED", "FAILED", "PASSED"],
        )
        self.assertEqual(
            [stage["name"] for stage in details["stages"]],
            ["01_first", "02_failed", "03_last"],
        )

    @patch("case_runner.set_screenshot_stage")
    @patch("case_runner.save_screenshot")
    def test_run_suite_does_not_count_auxiliary_cleanup_failures(
        self,
        save_screenshot_mock,
        _stage_mock,
    ):
        first_case = Mock(return_value={"stages": []})
        cleanup = Mock(side_effect=RuntimeError("cleanup failed"))
        second_case = Mock(return_value={"stages": []})

        details = case_runner.run_suite(
            [
                ("01_first", first_case),
                (
                    "01_5_cleanup",
                    cleanup,
                    {"reportable": False, "kind": "cleanup"},
                ),
                ("02_second", second_case),
            ]
        )

        first_case.assert_called_once_with()
        cleanup.assert_called_once_with()
        second_case.assert_called_once_with()
        save_screenshot_mock.assert_called_once_with("FAILED_error")
        self.assertEqual(details["status"], "PASSED")
        self.assertIsNone(details["error"])
        self.assertEqual(
            details["suite_summary"],
            {
                "total": 2,
                "passed": 2,
                "failed": 0,
            },
        )
        self.assertEqual(
            details["auxiliary_summary"],
            {
                "total": 1,
                "passed": 0,
                "failed": 1,
            },
        )
        self.assertFalse(details["suite_cases"][1]["reportable"])

    @patch("case_runner.generate_pdf_report")
    @patch("case_runner.generate_excel_report")
    @patch("case_runner.save_result")
    def test_run_case_marks_failed_suite_as_failed(
        self,
        save_result_mock,
        _excel_report_mock,
        _report_mock,
    ):
        case_function = Mock(
            return_value={
                "status": "FAILED",
                "error": "1 of 3 suite cases failed.",
                "suite_summary": {
                    "total": 3,
                    "passed": 2,
                    "failed": 1,
                },
                "suite_cases": [],
                "stages": [],
            }
        )

        success = case_runner.run_case("e2e_set_5", case_function)

        self.assertFalse(success)
        result = save_result_mock.call_args.args[0]
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["error"], "1 of 3 suite cases failed.")
        self.assertEqual(result["suite_summary"]["failed"], 1)

    @patch("case_runner.generate_pdf_report")
    @patch("case_runner.generate_excel_report")
    @patch("case_runner.save_result")
    def test_after_run_copies_pos_log_when_enabled(
        self,
        _save_result_mock,
        _excel_report_mock,
        _report_mock,
    ):
        self.after_run_enabled_mock.return_value = True
        case_function = Mock()

        success = case_runner.run_case("login", case_function)

        self.assertTrue(success)
        self.copy_pos_log_mock.assert_called_once_with(
            run_folder=case_runner.RUN_FOLDER
        )

    @patch("case_runner.generate_pdf_report")
    @patch("case_runner.generate_excel_report")
    @patch("case_runner.save_result")
    def test_after_run_log_copy_failure_does_not_fail_case(
        self,
        _save_result_mock,
        _excel_report_mock,
        _report_mock,
    ):
        self.after_run_enabled_mock.return_value = True
        self.copy_pos_log_mock.side_effect = RuntimeError("copy failed")
        case_function = Mock()

        success = case_runner.run_case("login", case_function)

        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
