import sys
import types
import unittest
import importlib
from unittest.mock import call, patch


applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None
applications_stub.open_windows_app = lambda: None

premium_close_stub = types.ModuleType("features.premium_close_app")
premium_close_stub.close_with_alt_f4 = lambda: None

kiosk_process_stub = types.ModuleType("features.kiosk_process")
kiosk_process_stub.force_close_kiosk_process = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

pyautogui_stub = types.ModuleType("pyautogui")
pyautogui_stub.press = lambda *args, **kwargs: None

_STUBBED_MODULES = {
    "features.applications": applications_stub,
    "features.premium_close_app": premium_close_stub,
    "features.kiosk_process": kiosk_process_stub,
    "screenshot": screenshot_stub,
    "pyautogui": pyautogui_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
windows_app_close_hung_up = importlib.import_module(
    "features.windows_app_close_hung_up"
)

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "applications",
        "premium_close_app",
        "kiosk_process",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class WindowsAppCloseHungUpFlowTests(unittest.TestCase):
    @patch("features.windows_app_close_hung_up.force_close_kiosk_process")
    @patch("features.windows_app_close_hung_up.close_with_alt_f4")
    @patch("features.windows_app_close_hung_up.save_screenshot")
    @patch("features.windows_app_close_hung_up.pyautogui.press")
    @patch("features.windows_app_close_hung_up.time.sleep")
    @patch("features.windows_app_close_hung_up.open_anydesk")
    @patch("features.windows_app_close_hung_up.open_windows_app")
    def test_hangs_up_then_returns_to_anydesk_and_closes_kiosk(
        self,
        open_windows_app_mock,
        open_anydesk_mock,
        _sleep_mock,
        press_mock,
        save_screenshot_mock,
        close_with_alt_f4_mock,
        force_close_kiosk_process_mock,
    ):
        windows_app_close_hung_up.run()

        open_windows_app_mock.assert_called_once_with()
        self.assertEqual(
            press_mock.call_args_list,
            [
                call("d"),
                call("c"),
            ],
        )
        open_anydesk_mock.assert_called_once_with()
        close_with_alt_f4_mock.assert_called_once_with()
        force_close_kiosk_process_mock.assert_called_once_with()
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("pump_simulator_descolgar_executed"),
                call("pump_simulator_colgar_executed"),
                call("return_anydesk"),
                call("step_5_alt_f4_close_attempt"),
                call("step_6_force_close_attempt"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
