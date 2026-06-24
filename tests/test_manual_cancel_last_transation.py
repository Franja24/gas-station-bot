import importlib
import sys
import types
import unittest
from unittest.mock import call, patch


clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_coordinates = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: None

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

pyautogui_stub = types.ModuleType("pyautogui")
pyautogui_stub.hotkey = lambda *args, **kwargs: None
pyautogui_stub.press = lambda *args, **kwargs: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

_STUBBED_MODULES = {
    "clicker": clicker_stub,
    "detector": detector_stub,
    "features.applications": applications_stub,
    "pyautogui": pyautogui_stub,
    "screenshot": screenshot_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
manual_cancel_last_transation = importlib.import_module(
    "features.manual_cancel_last_transation"
)

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module


class ManualCancelLastTransationTests(unittest.TestCase):
    @patch("features.manual_cancel_last_transation.save_screenshot")
    @patch("features.manual_cancel_last_transation.click_image")
    @patch("features.manual_cancel_last_transation.click_coordinates")
    @patch(
        "features.manual_cancel_last_transation.find_image",
        return_value=object(),
    )
    @patch("features.manual_cancel_last_transation.assert_image_visible")
    @patch("features.manual_cancel_last_transation.time.sleep")
    @patch("features.manual_cancel_last_transation.pyautogui.hotkey")
    @patch("features.manual_cancel_last_transation.pyautogui.press")
    @patch("features.manual_cancel_last_transation.open_anydesk")
    def test_opens_settings_and_cancels_latest_transaction(
        self,
        open_anydesk_mock,
        press_mock,
        hotkey_mock,
        sleep_mock,
        assert_image_visible_mock,
        find_image_mock,
        click_coordinates_mock,
        click_image_mock,
        save_screenshot_mock,
    ):
        manual_cancel_last_transation.run()

        open_anydesk_mock.assert_called_once_with()
        hotkey_mock.assert_called_once_with("alt", "space")
        self.assertEqual(
            click_coordinates_mock.call_args_list,
            [
                call(640, 400),
            ],
        )
        self.assertEqual(
            press_mock.call_args_list,
            [
                call("esc"),
                call("x"),
                call("space"),
                call("left"),
                call("enter"),
                call("tab"),
                call("tab"),
                call("enter"),
            ],
        )
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "pump_out_of_service_title.png",
                    timeout=3,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "employee_settings_button.png",
                    timeout=3,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "settings_transaction_log_option.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "transaction_log_first_row_marker.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "cancel_transaction_button.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "confirm_cancel_transaction_button.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
            ],
        )
        self.assertEqual(
            find_image_mock.call_args_list,
            [
                call("employee_settings_button.png", timeout=3),
                call("employee_settings_button.png", timeout=1),
                call("employee_settings_button.png", timeout=1),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call(
                    "settings_transaction_log_option.png",
                    confidence=0.80,
                    timeout=10,
                ),
                call(
                    "transaction_log_title.png",
                    confidence=0.80,
                    timeout=10,
                ),
                call(
                    "transaction_summary_title.png",
                    confidence=0.80,
                    timeout=10,
                ),
                call(
                    "confirm_cancel_transaction_button.png",
                    confidence=0.80,
                    timeout=10,
                ),
            ],
        )
        self.assertIn(call(0.2), sleep_mock.call_args_list)
        self.assertIn(call(3), sleep_mock.call_args_list)
        save_screenshot_mock.assert_called_with(
            "step_5_cancel_transaction_confirmed"
        )


if __name__ == "__main__":
    unittest.main()
