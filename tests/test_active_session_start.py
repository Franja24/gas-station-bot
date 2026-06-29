import sys
import types
import unittest
from unittest.mock import call, patch


clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: None

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("detector", detector_stub)
sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("screenshot", screenshot_stub)

from features import active_session_start


class ActiveSessionStartTests(unittest.TestCase):
    @patch("features.active_session_start.save_screenshot")
    @patch("features.active_session_start.assert_image_visible")
    @patch("features.active_session_start.click_image")
    @patch("features.active_session_start.find_image")
    @patch("features.active_session_start.dismiss_windows_start_menu")
    @patch("features.active_session_start.open_anydesk")
    def test_clicks_iniciar_and_validates_product_selection(
        self,
        open_anydesk_mock,
        dismiss_windows_start_menu_mock,
        find_image_mock,
        click_image_mock,
        assert_image_visible_mock,
        save_screenshot_mock,
    ):
        find_image_mock.side_effect = [
            None,
            None,
            object(),
            object(),
            object(),
            object(),
        ]

        active_session_start.run()

        open_anydesk_mock.assert_called_once_with()
        dismiss_windows_start_menu_mock.assert_called_once_with()
        click_image_mock.assert_called_once_with(
            "start.png",
            confidence=0.80,
            timeout=10,
            use_coordinates=False,
            use_region=False,
        )
        assert_image_visible_mock.assert_not_called()
        save_screenshot_mock.assert_called_once_with(
            "start_clicked_product_selection_visible"
        )

    @patch("features.active_session_start.save_screenshot")
    @patch("features.active_session_start.assert_image_visible")
    @patch("features.active_session_start.click_image")
    @patch("features.active_session_start.find_image")
    @patch("features.active_session_start.dismiss_windows_start_menu")
    @patch("features.active_session_start.open_anydesk")
    def test_skips_start_when_product_selection_is_already_visible(
        self,
        _open_anydesk_mock,
        dismiss_windows_start_menu_mock,
        find_image_mock,
        click_image_mock,
        assert_image_visible_mock,
        save_screenshot_mock,
    ):
        find_image_mock.side_effect = [object(), object()]

        active_session_start.run()

        dismiss_windows_start_menu_mock.assert_called_once_with()
        click_image_mock.assert_not_called()
        assert_image_visible_mock.assert_not_called()
        save_screenshot_mock.assert_called_once_with(
            "product_selection_already_visible"
        )

    @patch("features.active_session_start.time.sleep")
    @patch("features.active_session_start.pyautogui.press")
    def test_dismisses_windows_start_menu_with_escape(
        self,
        press_mock,
        sleep_mock,
    ):
        active_session_start.dismiss_windows_start_menu()

        press_mock.assert_called_once_with("esc")
        sleep_mock.assert_called_once_with(0.5)


if __name__ == "__main__":
    unittest.main()
