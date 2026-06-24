import unittest
import sys
import types
from unittest.mock import call, patch


clicker_stub = types.ModuleType("clicker")
clicker_stub.ClickError = RuntimeError
clicker_stub.click_image = lambda *args, **kwargs: True

detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: object()

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("detector", detector_stub)
sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("screenshot", screenshot_stub)

from features import start_kiosk_session


class StartKioskSessionTests(unittest.TestCase):
    @patch("features.start_kiosk_session.save_screenshot")
    @patch("features.start_kiosk_session.find_image")
    @patch("features.start_kiosk_session.click_image")
    @patch("features.start_kiosk_session.open_anydesk")
    def test_clicks_iniciar_and_accepts_login_screen(
        self,
        open_anydesk_mock,
        click_image_mock,
        find_image_mock,
        save_screenshot_mock,
    ):
        find_image_mock.side_effect = [None, object()]

        start_kiosk_session.run()

        open_anydesk_mock.assert_called_once_with()
        click_image_mock.assert_not_called()
        self.assertEqual(
            [call.args[0] for call in find_image_mock.call_args_list],
            ["premium.png", "login_button.png"],
        )
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("step_0_login_already_visible"),
            ],
        )

    @patch("features.start_kiosk_session.save_screenshot")
    @patch("features.start_kiosk_session.find_image")
    @patch("features.start_kiosk_session.click_image")
    @patch("features.start_kiosk_session.open_anydesk")
    def test_clicks_iniciar_and_accepts_selection_screen(
        self,
        _open_anydesk_mock,
        _click_image_mock,
        find_image_mock,
        save_screenshot_mock,
    ):
        find_image_mock.side_effect = [None, None, None, object()]

        start_kiosk_session.run()

        self.assertEqual(
            [call.args[0] for call in find_image_mock.call_args_list],
            [
                "premium.png",
                "login_button.png",
                "login_button.png",
                "premium.png",
            ],
        )
        save_screenshot_mock.assert_called_with("step_2_selection_visible")

    @patch("features.start_kiosk_session.save_screenshot")
    @patch("features.start_kiosk_session.find_image", return_value=object())
    @patch("features.start_kiosk_session.click_image")
    @patch("features.start_kiosk_session.open_anydesk")
    def test_skips_iniciar_when_selection_is_already_visible(
        self,
        _open_anydesk_mock,
        click_image_mock,
        find_image_mock,
        save_screenshot_mock,
    ):
        start_kiosk_session.run()

        find_image_mock.assert_called_once_with("premium.png", timeout=2)
        click_image_mock.assert_not_called()
        save_screenshot_mock.assert_called_once_with(
            "step_0_selection_already_visible"
        )


if __name__ == "__main__":
    unittest.main()
