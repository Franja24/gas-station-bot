import importlib
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

_STUBBED_MODULES = {
    "features.applications": applications_stub,
    "screenshot": screenshot_stub,
    "pyautogui": pyautogui_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
windows_app_hang_up = importlib.import_module("features.windows_app_hang_up")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    feature_module = getattr(features_package, "applications", None)
    if feature_module in _STUBBED_MODULES.values():
        delattr(features_package, "applications")


class WindowsAppHangUpTests(unittest.TestCase):
    @patch("features.windows_app_hang_up.save_screenshot")
    @patch("features.windows_app_hang_up.pyautogui.press")
    @patch("features.windows_app_hang_up.time.sleep")
    @patch("features.windows_app_hang_up.open_anydesk")
    @patch("features.windows_app_hang_up.open_windows_app")
    def test_hangs_up_and_returns_to_anydesk(
        self,
        open_windows_app_mock,
        open_anydesk_mock,
        _sleep_mock,
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
                call("pump_simulator_colgar_after_kiosk_close"),
                call("return_anydesk_after_hang_up"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
