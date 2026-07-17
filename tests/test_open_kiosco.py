import sys
import types
import unittest
from unittest.mock import call, patch

clicker_stub = types.ModuleType("clicker")
clicker_stub.ClickError = RuntimeError
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_coordinates = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True
clicker_stub.double_click_coordinates = lambda *args, **kwargs: True

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

pyautogui_stub = types.ModuleType("pyautogui")
pyautogui_stub.hotkey = lambda *args, **kwargs: None
pyautogui_stub.press = lambda *args, **kwargs: None
pyautogui_stub.click = lambda *args, **kwargs: None
pyautogui_stub.size = lambda: (1920, 1200)

sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("screenshot", screenshot_stub)
sys.modules.setdefault("pyautogui", pyautogui_stub)

from features import open_kiosco


class OpenKioscoFlowTests(unittest.TestCase):
    @patch("features.open_kiosco.save_screenshot")
    @patch("features.open_kiosco.is_kiosk_ready", side_effect=[False, True])
    @patch("features.open_kiosco.pyautogui.click")
    @patch("features.open_kiosco.pyautogui.size", return_value=(1920, 1200))
    @patch("features.open_kiosco.time.sleep")
    @patch("features.open_kiosco.open_anydesk")
    def test_wakes_existing_kiosk_before_trying_to_launch_it(
        self,
        open_anydesk_mock,
        _sleep_mock,
        _size_mock,
        click_mock,
        is_kiosk_ready_mock,
        save_screenshot_mock,
    ):
        open_kiosco.run()

        open_anydesk_mock.assert_called_once_with()
        click_mock.assert_called_once_with(960, 600)
        self.assertEqual(is_kiosk_ready_mock.call_count, 2)
        save_screenshot_mock.assert_any_call(
            "step_0_kiosk_screensaver_wake_attempt"
        )
        save_screenshot_mock.assert_any_call("step_0_kiosk_awake_and_ready")

    @patch("features.open_kiosco.assert_image_visible")
    @patch("features.open_kiosco.save_screenshot")
    @patch("features.open_kiosco.find_image")
    @patch("features.open_kiosco.double_click_coordinates")
    @patch("features.open_kiosco.pyautogui.press")
    @patch("features.open_kiosco.subprocess.run")
    @patch("features.open_kiosco.pyautogui.hotkey")
    @patch("features.open_kiosco.time.sleep")
    @patch("features.open_kiosco.open_anydesk")
    def test_opens_kiosk_from_windows_run_dialog(
        self,
        open_anydesk_mock,
        _sleep_mock,
        hotkey_mock,
        subprocess_run_mock,
        press_mock,
        double_click_coordinates_mock,
        find_image_mock,
        save_screenshot_mock,
        assert_image_visible_mock,
    ):
        find_image_mock.return_value = object()

        open_kiosco.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            hotkey_mock.call_args_list,
            [
                call("command", "r"),
                call("ctrl", "v"),
                call("command", "r"),
                call("ctrl", "v"),
            ],
        )
        self.assertEqual(
            subprocess_run_mock.call_args_list,
            [
                call(
                    ["pbcopy"],
                    input=open_kiosco.REMOTE_WINDOW_CLEANUP_COMMAND,
                    text=True,
                    check=True,
                ),
                call(
                    ["pbcopy"],
                    input=open_kiosco.PETRO_KIOSK_RUN_COMMAND,
                    text=True,
                    check=True,
                ),
            ],
        )
        self.assertEqual(
            press_mock.call_args_list,
            [
                call("enter"),
                call("enter"),
            ],
        )
        double_click_coordinates_mock.assert_not_called()
        assert_image_visible_mock.assert_not_called()
        save_screenshot_mock.assert_any_call("step_1_run_dialog_launch_attempt")

    @patch("features.open_kiosco.assert_image_visible")
    @patch("features.open_kiosco.save_screenshot")
    @patch("features.open_kiosco.find_image", return_value=None)
    @patch("features.open_kiosco.double_click_coordinates")
    @patch("features.open_kiosco.pyautogui.press")
    @patch("features.open_kiosco.subprocess.run")
    @patch("features.open_kiosco.pyautogui.hotkey")
    @patch("features.open_kiosco.time.sleep")
    @patch("features.open_kiosco.open_anydesk")
    def test_falls_back_to_desktop_icon_when_run_dialog_does_not_open_kiosk(
        self,
        _open_anydesk_mock,
        _sleep_mock,
        hotkey_mock,
        _subprocess_run_mock,
        _press_mock,
        double_click_coordinates_mock,
        _find_image_mock,
        save_screenshot_mock,
        _assert_image_visible_mock,
    ):
        open_kiosco.run()

        self.assertEqual(
            hotkey_mock.call_args_list,
            [
                call("command", "r"),
                call("ctrl", "v"),
                call("command", "r"),
                call("ctrl", "v"),
                call("command", "d"),
            ],
        )
        double_click_coordinates_mock.assert_called_once_with(
            *open_kiosco.PETRO_KIOSK_ICON_COORDINATES
        )
        save_screenshot_mock.assert_any_call("step_2_windows_desktop_visible")
        save_screenshot_mock.assert_any_call(
            "step_3_desktop_icon_launch_attempt"
        )

    @patch("features.open_kiosco.assert_image_visible")
    @patch("features.open_kiosco.click_image")
    @patch("features.open_kiosco.find_image")
    @patch("features.open_kiosco.time.sleep")
    def test_ensure_login_screen_clicks_iniciar_when_start_screen_is_visible(
        self,
        _sleep_mock,
        find_image_mock,
        click_image_mock,
        assert_image_visible_mock,
    ):
        find_image_mock.side_effect = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            object(),
            None,
            object(),
        ]

        result = open_kiosco.ensure_login_screen()

        self.assertTrue(result)
        click_image_mock.assert_called_once_with(
            "iniciar.png",
            confidence=0.85,
            timeout=5,
            use_coordinates=False,
            use_region=False,
        )
        assert_image_visible_mock.assert_not_called()

    @patch("features.open_kiosco.find_image")
    def test_ensure_login_screen_accepts_login_form(
        self,
        find_image_mock,
    ):
        find_image_mock.side_effect = [
            None,
            object(),
        ]

        result = open_kiosco.ensure_login_screen()

        self.assertTrue(result)

    @patch("features.open_kiosco.find_image")
    def test_ensure_login_screen_accepts_out_of_service_screen(
        self,
        find_image_mock,
    ):
        find_image_mock.side_effect = [
            None,
            None,
            None,
            object(),
        ]

        result = open_kiosco.ensure_login_screen()

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
