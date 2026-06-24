import importlib
import sys
import types
import unittest
from unittest.mock import call, patch


clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True

detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: None

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

premium_stub = types.ModuleType("features.premium")
premium_stub.click_asset = lambda *args, **kwargs: None
premium_stub.handle_benefits_or_payment = lambda *args, **kwargs: None
premium_stub.wait_for_benefits_or_payment = lambda *args, **kwargs: "payment"

premium_close_app_stub = types.ModuleType("features.premium_close_app")
premium_close_app_stub.close_with_alt_f4 = lambda: None

pyautogui_stub = types.ModuleType("pyautogui")
pyautogui_stub.hotkey = lambda *args, **kwargs: None
pyautogui_stub.press = lambda *args, **kwargs: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

_STUBBED_MODULES = {
    "clicker": clicker_stub,
    "detector": detector_stub,
    "features.applications": applications_stub,
    "features.premium": premium_stub,
    "features.premium_close_app": premium_close_app_stub,
    "pyautogui": pyautogui_stub,
    "screenshot": screenshot_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
payment_screen_close_app = importlib.import_module(
    "features.payment_screen_close_app"
)

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module


class PaymentScreenCloseAppTests(unittest.TestCase):
    @patch("features.payment_screen_close_app.save_screenshot")
    @patch("features.payment_screen_close_app.force_close_kiosk_process")
    @patch("features.payment_screen_close_app.find_image", return_value=None)
    @patch("features.payment_screen_close_app.close_with_alt_f4")
    @patch("features.payment_screen_close_app.time.sleep")
    @patch("features.payment_screen_close_app.handle_benefits_or_payment")
    @patch(
        "features.payment_screen_close_app.wait_for_benefits_or_payment",
        return_value="payment",
    )
    @patch("features.payment_screen_close_app.assert_image_visible")
    @patch("features.payment_screen_close_app.click_asset")
    @patch("features.payment_screen_close_app.open_anydesk")
    def test_closes_kiosk_at_payment_screen_before_windows_app(
        self,
        open_anydesk_mock,
        click_asset_mock,
        assert_image_visible_mock,
        wait_for_benefits_or_payment_mock,
        handle_benefits_or_payment_mock,
        sleep_mock,
        close_with_alt_f4_mock,
        find_image_mock,
        force_close_kiosk_process_mock,
        save_screenshot_mock,
    ):
        payment_screen_close_app.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            click_asset_mock.call_args_list,
            [
                call("premium.png", timeout=10),
                call("amount_1250.png", timeout=10),
                call("continue_button.png", timeout=10),
                call("card.png", timeout=10),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call("amount_1250.png", confidence=0.80, timeout=10),
                call("continue_button.png", confidence=0.80, timeout=10),
                call("card.png", confidence=0.80, timeout=10),
            ],
        )
        wait_for_benefits_or_payment_mock.assert_called_once_with()
        handle_benefits_or_payment_mock.assert_called_once_with("payment")
        sleep_mock.assert_called_once_with(5)
        close_with_alt_f4_mock.assert_called_once_with()
        self.assertGreaterEqual(find_image_mock.call_count, 8)
        force_close_kiosk_process_mock.assert_called_once_with()
        save_screenshot_mock.assert_any_call("step_4_payment_screen_visible")
        save_screenshot_mock.assert_any_call(
            "step_5_card_clicked_wait_before_close"
        )
        save_screenshot_mock.assert_any_call("step_7_force_close_attempt")
        save_screenshot_mock.assert_called_with(
            "step_8_kiosk_closed_confirmed"
        )

    @patch("features.payment_screen_close_app.save_screenshot")
    @patch("features.payment_screen_close_app.force_close_kiosk_process")
    @patch("features.payment_screen_close_app.close_with_alt_f4")
    @patch("features.payment_screen_close_app.time.sleep")
    @patch("features.payment_screen_close_app.handle_benefits_or_payment")
    @patch(
        "features.payment_screen_close_app.wait_for_benefits_or_payment",
        return_value="payment",
    )
    @patch("features.payment_screen_close_app.assert_image_visible")
    @patch("features.payment_screen_close_app.click_asset")
    @patch("features.payment_screen_close_app.open_anydesk")
    def test_force_closes_kiosk_when_alt_f4_does_not_close_it(
        self,
        _open_anydesk_mock,
        _click_asset_mock,
        _assert_image_visible_mock,
        _wait_for_benefits_or_payment_mock,
        _handle_benefits_or_payment_mock,
        _sleep_mock,
        _close_with_alt_f4_mock,
        force_close_kiosk_process_mock,
        save_screenshot_mock,
    ):
        marker_seen = {"card.png": 0}

        def find_image_side_effect(image_name, **_kwargs):
            if image_name == "card.png" and marker_seen["card.png"] == 0:
                marker_seen["card.png"] += 1
                return object()

            return None

        with patch(
            "features.payment_screen_close_app.find_image",
            side_effect=find_image_side_effect,
        ):
            payment_screen_close_app.run()

        force_close_kiosk_process_mock.assert_called_once_with()
        save_screenshot_mock.assert_any_call("step_7_force_close_attempt")
        save_screenshot_mock.assert_called_with(
            "step_8_kiosk_closed_confirmed"
        )


if __name__ == "__main__":
    unittest.main()
