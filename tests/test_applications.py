import unittest
from unittest.mock import patch

from features import applications


class OpenAnyDeskTests(unittest.TestCase):
    @patch("features.applications.save_screenshot")
    @patch("features.applications._frontmost_app_name", return_value="AnyDesk")
    @patch("features.applications._activate_app")
    def test_open_anydesk_verifies_frontmost_app(
        self,
        activate_app_mock,
        _frontmost_app_name_mock,
        save_screenshot_mock,
    ):
        applications.open_anydesk()

        activate_app_mock.assert_called_once_with(applications.ANYDESK_BUNDLE_ID)
        save_screenshot_mock.assert_called_once_with("anydesk_opened")

    @patch("features.applications.time.sleep")
    @patch("features.applications.time.monotonic", side_effect=[0, 1, 11])
    @patch("features.applications.save_screenshot")
    @patch("features.applications._frontmost_app_name", return_value="Codex")
    @patch("features.applications._activate_app")
    def test_open_anydesk_stops_when_app_is_not_frontmost(
        self,
        _activate_app_mock,
        _frontmost_app_name_mock,
        save_screenshot_mock,
        _monotonic_mock,
        _sleep_mock,
    ):
        with self.assertRaisesRegex(RuntimeError, "app al frente: Codex"):
            applications.open_anydesk()

        save_screenshot_mock.assert_called_once_with("anydesk_not_frontmost")


if __name__ == "__main__":
    unittest.main()
