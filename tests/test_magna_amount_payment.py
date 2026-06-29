import importlib
import sys
import types
import unittest
from unittest.mock import call, patch


clicker_stub = types.ModuleType("clicker")
clicker_stub.ClickError = RuntimeError
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_coordinates = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: None

premium_stub = types.ModuleType("features.premium")
premium_stub.handle_benefits_or_payment = lambda *args, **kwargs: None
premium_stub.handle_payment_result = lambda *args, **kwargs: None
premium_stub.wait_for_benefits_or_payment = lambda *args, **kwargs: "payment"
premium_stub.wait_for_payment_result = lambda *args, **kwargs: "success"

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

_STUBBED_MODULES = {
    "clicker": clicker_stub,
    "detector": detector_stub,
    "features.applications": applications_stub,
    "features.premium": premium_stub,
    "screenshot": screenshot_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
magna_amount_payment = importlib.import_module("features.magna_amount_payment")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "applications",
        "premium",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class MagnaAmountPaymentFlowTests(unittest.TestCase):
    @patch("features.magna_amount_payment.handle_benefits_or_payment")
    @patch("features.magna_amount_payment.handle_payment_result")
    @patch("features.magna_amount_payment.wait_for_benefits_or_payment")
    @patch("features.magna_amount_payment.wait_for_payment_result")
    @patch("features.magna_amount_payment.find_image")
    @patch("features.magna_amount_payment.assert_image_visible")
    @patch("features.magna_amount_payment.save_screenshot")
    @patch("features.magna_amount_payment.time.sleep")
    @patch("features.magna_amount_payment.click_coordinates")
    @patch("features.magna_amount_payment.click_image")
    @patch("features.magna_amount_payment.open_anydesk")
    def test_enters_amount_100_button_by_button_and_completes_payment(
        self,
        open_anydesk_mock,
        click_image_mock,
        click_coordinates_mock,
        _sleep_mock,
        _save_screenshot_mock,
        assert_image_visible_mock,
        find_image_mock,
        wait_for_payment_result_mock,
        wait_for_benefits_or_payment_mock,
        handle_payment_result_mock,
        handle_benefits_or_payment_mock,
    ):
        wait_for_benefits_or_payment_mock.return_value = "payment"
        wait_for_payment_result_mock.return_value = "success"
        find_image_mock.return_value = object()

        magna_amount_payment.run_amount_payment("100", "magna_amount_100")

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "magna.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "charge_type_amount_tab.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "charge_amount_input_field.png",
                    timeout=10,
                    use_coordinates=True,
                    use_region=False,
                ),
                call(
                    "continue_button.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "card.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
            ],
        )
        self.assertEqual(
            click_coordinates_mock.call_args_list,
            [
                call(526, 302),
                call(638, 433),
                call(638, 433),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call("continue_button.png", confidence=0.80, timeout=10),
                call("card.png", confidence=0.80, timeout=10),
            ],
        )
        wait_for_benefits_or_payment_mock.assert_called_once_with()
        handle_benefits_or_payment_mock.assert_called_once_with("payment")
        wait_for_payment_result_mock.assert_called_once_with()
        handle_payment_result_mock.assert_called_once_with("success")

    @patch("features.magna_amount_payment.click_image")
    def test_asset_click_falls_back_to_calibrated_coordinates(
        self,
        click_image_mock,
    ):
        click_image_mock.side_effect = [
            magna_amount_payment.ClickError("missing asset"),
            True,
        ]

        result = magna_amount_payment.click_asset_or_calibrated(
            "one_button.png",
            timeout=10,
        )

        self.assertTrue(result)
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "one_button.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "one_button.png",
                    timeout=10,
                    use_coordinates=True,
                    use_region=False,
                ),
            ],
        )


if __name__ == "__main__":
    unittest.main()
