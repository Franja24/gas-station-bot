import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import call, patch


clicker_stub = types.ModuleType("clicker")
clicker_stub.ClickError = RuntimeError

detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: SimpleNamespace(x=10, y=20)

pyautogui_stub = types.ModuleType("pyautogui")
pyautogui_stub.click = lambda *args, **kwargs: None
pyautogui_stub.press = lambda *args, **kwargs: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("detector", detector_stub)
sys.modules.setdefault("pyautogui", pyautogui_stub)
sys.modules.setdefault("screenshot", screenshot_stub)

from features import cancel_last_operation


class CancelLastOperationTests(unittest.TestCase):
    @patch("features.cancel_last_operation.save_screenshot")
    @patch("features.cancel_last_operation.click_relative_to_asset")
    @patch("features.cancel_last_operation.find_asset_local_center")
    @patch(
        "features.cancel_last_operation.find_image",
        return_value=SimpleNamespace(x=10, y=20),
    )
    @patch("features.cancel_last_operation.pyautogui.click")
    @patch("features.cancel_last_operation.pyautogui.press")
    @patch("features.cancel_last_operation.time.sleep")
    def test_opens_last_operation_from_out_of_service_screen(
        self,
        sleep_mock,
        press_mock,
        click_mock,
        find_image_mock,
        find_asset_local_center_mock,
        click_relative_to_asset_mock,
        save_screenshot_mock,
    ):
        cancel_last_operation.run()

        press_mock.assert_called_once_with("space")
        self.assertEqual(
            find_image_mock.call_args_list,
            [
                call(
                    "settings_button.png",
                    timeout=15,
                ),
            ],
        )
        self.assertEqual(
            click_mock.call_args_list,
            [
                call(5, 10),
            ],
        )
        self.assertEqual(
            find_asset_local_center_mock.call_args_list,
            [
                call("transaction_registry_title.png", timeout=15),
                call("transaction_summary_title.png", timeout=15),
            ],
        )
        self.assertEqual(
            click_relative_to_asset_mock.call_args_list,
            [
                call(
                    "transaction_registry_button.png",
                    (160, 0),
                    timeout=15,
                ),
                call(
                    "transaction_registry_title.png",
                    (-100, 92),
                    timeout=15,
                ),
                call(
                    "transaction_summary_title.png",
                    (475, 202),
                    timeout=15,
                ),
            ],
        )
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("step_1_out_of_service_menu_opened"),
                call("step_2_settings_clicked"),
                call("step_3_transaction_registry_opened"),
                call("step_4_first_transaction_opened"),
                call("step_5_first_message_eye_clicked"),
            ],
        )
        self.assertEqual(
            sleep_mock.call_args_list,
            [
                call(1),
                call(1),
                call(1),
                call(1),
                call(1),
            ],
        )

    @patch("features.cancel_last_operation.save_screenshot")
    @patch(
        "features.cancel_last_operation.find_image",
        return_value=SimpleNamespace(x=10, y=20),
    )
    @patch("features.cancel_last_operation.pyautogui.click")
    @patch("features.cancel_last_operation.time.sleep")
    def test_go_back_clicks_regresar_asset(
        self,
        sleep_mock,
        click_mock,
        find_image_mock,
        save_screenshot_mock,
    ):
        cancel_last_operation.go_back()

        find_image_mock.assert_called_once_with("regresar_button.png", timeout=10)
        click_mock.assert_called_once_with(5, 10)
        sleep_mock.assert_called_once_with(1)
        save_screenshot_mock.assert_called_once_with("step_back_clicked")


if __name__ == "__main__":
    unittest.main()
