import unittest
from pathlib import Path
from unittest.mock import patch

from config.asset_aliases import get_image_candidates


class AssetAliasesTests(unittest.TestCase):
    @patch("config.asset_aliases.get_automation_platform", return_value="windows")
    def test_use_rfid_prefers_windows_asset(self, _platform_mock):
        candidates = get_image_candidates("use_rfid_button.png")

        self.assertEqual(
            candidates,
            ["use_rfid_button_windows.png", "use_rfid_button.png"],
        )
        self.assertTrue(
            (
                Path(__file__).resolve().parents[1]
                / "assets"
                / candidates[0]
            ).is_file()
        )

    @patch("config.asset_aliases.get_automation_platform", return_value="windows")
    def test_sevenly_qr_assets_prefer_windows_captures(self, _platform_mock):
        for logical_name, windows_name in (
            ("sevenly_qr_option.png", "sevenly_qr_option_windows.png"),
            ("sevenly_qr_waiting.png", "sevenly_qr_waiting_windows.png"),
            ("sevenly_qr_scanner.png", "sevenly_qr_scanner_windows.png"),
            ("change_employee_title.png", "change_employee_title_windows.png"),
            (
                "change_employee_activate_button.png",
                "change_employee_activate_button_windows.png",
            ),
            ("activate_unit_button.png", "activate_unit_button_windows.png"),
            ("no_benefits_button.png", "no_benefits_button_windows.png"),
            ("regresar_button.png", "regresar_button_windows.png"),
            (
                "declined_response_eye_button.png",
                "declined_response_eye_button_windows.png",
            ),
            ("metadata_response_title.png", "metadata_response_title_windows.png"),
            ("metadata_close_button.png", "metadata_close_button_windows.png"),
            ("start.png", "start_windows.png"),
        ):
            candidates = get_image_candidates(logical_name)
            self.assertEqual(candidates[0], windows_name)
            self.assertTrue(
                (
                    Path(__file__).resolve().parents[1]
                    / "assets"
                    / windows_name
                ).is_file()
            )


if __name__ == "__main__":
    unittest.main()
