import importlib
import sys
import types
import unittest
from unittest.mock import call, patch


applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None
applications_stub.open_windows_app = lambda: None

kiosk_process_stub = types.ModuleType("features.kiosk_process")
kiosk_process_stub.force_close_kiosk_process = lambda: None

premium_close_stub = types.ModuleType("features.premium_close_app")
premium_close_stub.close_with_alt_f4 = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

pyautogui_stub = types.ModuleType("pyautogui")
pyautogui_stub.press = lambda *args, **kwargs: None

_STUBBED_MODULES = {
    "features.applications": applications_stub,
    "features.kiosk_process": kiosk_process_stub,
    "features.premium_close_app": premium_close_stub,
    "screenshot": screenshot_stub,
    "pyautogui": pyautogui_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
windows_app_unhook_close = importlib.import_module(
    "features.windows_app_unhook_close"
)

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module


class WindowsAppUnhookCloseTests(unittest.TestCase):
    @patch("features.windows_app_unhook_close.force_close_kiosk_process")
    @patch("features.windows_app_unhook_close.close_with_alt_f4")
    @patch("features.windows_app_unhook_close.save_screenshot")
    @patch("features.windows_app_unhook_close.pyautogui.press")
    @patch("features.windows_app_unhook_close.time.sleep")
    @patch("features.windows_app_unhook_close.open_anydesk")
    @patch("features.windows_app_unhook_close.open_windows_app")
    def test_unhooks_hose_and_closes_kiosk(
        self,
        open_windows_app_mock,
        open_anydesk_mock,
        _sleep_mock,
        press_mock,
        save_screenshot_mock,
        close_with_alt_f4_mock,
        force_close_kiosk_process_mock,
    ):
        windows_app_unhook_close.run()

        open_windows_app_mock.assert_called_once_with()
        press_mock.assert_called_once_with("d")
        open_anydesk_mock.assert_called_once_with()
        close_with_alt_f4_mock.assert_called_once_with()
        force_close_kiosk_process_mock.assert_called_once_with()
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("pump_simulator_descolgar_executed"),
                call("return_anydesk"),
                call("step_2_alt_f4_close_attempt"),
                call("step_3_force_close_attempt"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
