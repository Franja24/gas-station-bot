import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import screenshot


class ReportTests(unittest.TestCase):
    def test_result_json_and_pdf_are_generated(self):
        result = {
            "run_id": "test_run",
            "case_name": "login",
            "status": "FAILED",
            "started_at": "2026-06-05T10:00:00",
            "finished_at": "2026-06-05T10:00:01",
            "duration_seconds": 1.0,
            "error": "ClickError: expected <premium.png>",
            "stages": [
                {
                    "name": "01_login",
                    "status": "PASSED",
                    "duration_seconds": 0.5,
                },
                {
                    "name": "02_premium",
                    "status": "FAILED",
                    "duration_seconds": 0.5,
                },
            ],
        }

        with tempfile.TemporaryDirectory() as temp_directory:
            run_folder = Path(temp_directory)
            screenshots_folder = run_folder / "screenshots"
            screenshots_folder.mkdir()

            with (
                patch.object(screenshot, "RUN_FOLDER", run_folder),
                patch.object(
                    screenshot,
                    "SCREENSHOTS_FOLDER",
                    screenshots_folder,
                ),
            ):
                result_path = screenshot.save_result(result)
                report_path = screenshot.generate_pdf_report(result)

            saved_result = json.loads(result_path.read_text(encoding="utf-8"))

            self.assertEqual(saved_result["status"], "FAILED")
            self.assertTrue(report_path.is_file())
            self.assertGreater(report_path.stat().st_size, 0)

    def test_screenshot_name_includes_current_stage(self):
        image = Mock()

        with tempfile.TemporaryDirectory() as temp_directory:
            screenshots_folder = Path(temp_directory)

            with (
                patch.object(
                    screenshot,
                    "SCREENSHOTS_FOLDER",
                    screenshots_folder,
                ),
                patch.object(
                    screenshot.pyautogui,
                    "screenshot",
                    return_value=image,
                ),
                patch.object(screenshot, "_SCREENSHOT_SEQUENCE", 0),
            ):
                screenshot.set_screenshot_case(None)
                screenshot.set_screenshot_stage("02_premium")
                screenshot_path = screenshot.save_screenshot("anydesk_opened")
                screenshot.set_screenshot_stage(None)

        self.assertEqual(
            screenshot_path.name,
            "001__02_premium__anydesk_opened.png",
        )
        image.save.assert_called_once()

    def test_screenshot_name_includes_current_case_and_stage(self):
        image = Mock()

        with tempfile.TemporaryDirectory() as temp_directory:
            screenshots_folder = Path(temp_directory)

            with (
                patch.object(
                    screenshot,
                    "SCREENSHOTS_FOLDER",
                    screenshots_folder,
                ),
                patch.object(
                    screenshot.pyautogui,
                    "screenshot",
                    return_value=image,
                ),
                patch.object(screenshot, "_SCREENSHOT_SEQUENCE", 0),
            ):
                screenshot.set_screenshot_case("TC01_normal_magna_1250")
                screenshot.set_screenshot_stage("00_prepare_product_selection")
                screenshot_path = screenshot.save_screenshot("ready")
                screenshot.set_screenshot_stage(None)
                screenshot.set_screenshot_case(None)

        self.assertEqual(
            screenshot_path.name,
            "001__TC01_normal_magna_1250__00_prepare_product_selection__ready.png",
        )
        image.save.assert_called_once()


if __name__ == "__main__":
    unittest.main()
