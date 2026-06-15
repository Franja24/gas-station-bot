import sys
import types
import unittest
from unittest.mock import call, patch

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None
applications_stub.open_windows_app = lambda: None

premium_close_stub = types.ModuleType("features.premium_close_app")
premium_close_stub.close_with_alt_f4 = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

pyautogui_stub = types.ModuleType("pyautogui")
pyautogui_stub.press = lambda *args, **kwargs: None

sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("features.premium_close_app", premium_close_stub)
sys.modules.setdefault("screenshot", screenshot_stub)
sys.modules.setdefault("pyautogui", pyautogui_stub)

from features import windows_app_close_app


class WindowsAppCloseAppFlowTests(unittest.TestCase):
    @patch("features.windows_app_close_app.close_with_alt_f4")
    @patch("features.windows_app_close_app.save_screenshot")
    @patch("features.windows_app_close_app.pyautogui.press")
    @patch("features.windows_app_close_app.time.sleep")
    @patch("features.windows_app_close_app.open_anydesk")
    @patch("features.windows_app_close_app.open_windows_app")
    def test_runs_pump_then_returns_to_anydesk_and_closes_kiosk(
        self,
        open_windows_app_mock,
        open_anydesk_mock,
        _sleep_mock,
        press_mock,
        save_screenshot_mock,
        close_with_alt_f4_mock,
    ):
        windows_app_close_app.run()

        open_windows_app_mock.assert_called_once_with()
        self.assertEqual(
            press_mock.call_args_list,
            [
                call("d"),
                call("g"),
            ],
        )
        open_anydesk_mock.assert_called_once_with()
        close_with_alt_f4_mock.assert_called_once_with()
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("pump_simulator_descolgar_executed"),
                call("pump_simulator_gatilo_executed"),
                call("return_anydesk"),
                call("step_3_alt_f4_close_attempt"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
