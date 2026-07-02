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

from features import windows_app_close_hung_up


class WindowsAppCloseHungUpFlowTests(unittest.TestCase):
    @patch("features.windows_app_close_hung_up.close_with_alt_f4")
    @patch("features.windows_app_close_hung_up.save_screenshot")
    @patch("features.windows_app_close_hung_up.pyautogui.press")
    @patch("features.windows_app_close_hung_up.time.sleep")
    @patch("features.windows_app_close_hung_up.open_anydesk")
    @patch("features.windows_app_close_hung_up.open_windows_app")
    def test_hangs_off_then_returns_to_anydesk_and_closes_kiosk(
        self,
        open_windows_app_mock,
        open_anydesk_mock,
        _sleep_mock,
        press_mock,
        save_screenshot_mock,
        close_with_alt_f4_mock,
    ):
        windows_app_close_hung_up.run()

        open_windows_app_mock.assert_called_once_with()
        self.assertEqual(
            press_mock.call_args_list,
            [
                call("d"),
            ],
        )
        open_anydesk_mock.assert_called_once_with()
        close_with_alt_f4_mock.assert_called_once_with()
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("pump_simulator_descolgar_executed"),
                call("return_anydesk"),
                call("step_4_alt_f4_close_attempt"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
