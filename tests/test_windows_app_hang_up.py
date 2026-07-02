import sys
import types
import unittest
from unittest.mock import call, patch


applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None
applications_stub.open_windows_app = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

pyautogui_stub = types.ModuleType("pyautogui")
pyautogui_stub.press = lambda *args, **kwargs: None

sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("screenshot", screenshot_stub)
sys.modules.setdefault("pyautogui", pyautogui_stub)

from features import windows_app_hang_up


class WindowsAppHangUpFlowTests(unittest.TestCase):
    @patch("features.windows_app_hang_up.save_screenshot")
    @patch("features.windows_app_hang_up.pyautogui.press")
    @patch("features.windows_app_hang_up.time.sleep")
    @patch("features.windows_app_hang_up.open_anydesk")
    @patch("features.windows_app_hang_up.open_windows_app")
    def test_hangs_up_then_returns_to_anydesk(
        self,
        open_windows_app_mock,
        open_anydesk_mock,
        sleep_mock,
        press_mock,
        save_screenshot_mock,
    ):
        windows_app_hang_up.run()

        open_windows_app_mock.assert_called_once_with()
        press_mock.assert_called_once_with("c")
        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("pump_simulator_colgar_executed"),
                call("return_anydesk_after_colgar"),
            ],
        )
        self.assertEqual(
            sleep_mock.call_args_list,
            [
                call(2),
                call(5),
            ],
        )


if __name__ == "__main__":
    unittest.main()
