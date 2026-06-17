import importlib
import sys
import types
import unittest
from unittest.mock import call, patch


clicker_stub = types.ModuleType("clicker")
clicker_stub.ClickError = RuntimeError
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

premium_stub = types.ModuleType("features.premium")
premium_stub.handle_benefits_or_payment = lambda *args, **kwargs: None
premium_stub.wait_for_benefits_or_payment = lambda *args, **kwargs: "payment"

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

_STUBBED_MODULES = {
    "clicker": clicker_stub,
    "features.applications": applications_stub,
    "features.premium": premium_stub,
    "screenshot": screenshot_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
change_type_charge = importlib.import_module("features.change_type_charge")

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


class ChangeTypeChargeFlowTests(unittest.TestCase):
    @patch("features.change_type_charge.handle_benefits_or_payment")
    @patch("features.change_type_charge.wait_for_benefits_or_payment")
    @patch("features.change_type_charge.assert_image_visible")
    @patch("features.change_type_charge.save_screenshot")
    @patch("features.change_type_charge.time.sleep")
    @patch("features.change_type_charge.click_image")
    @patch("features.change_type_charge.open_anydesk")
    def test_changes_charge_type_and_completes_payment(
        self,
        open_anydesk_mock,
        click_image_mock,
        _sleep_mock,
        _save_screenshot_mock,
        assert_image_visible_mock,
        wait_for_benefits_or_payment_mock,
        handle_benefits_or_payment_mock,
    ):
        wait_for_benefits_or_payment_mock.return_value = "payment"

        change_type_charge.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "premium.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "amount_1250.png",
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
                    "charge_amount_500.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "charge_type_liters_tab.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "charge_liters_20.png",
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
            assert_image_visible_mock.call_args_list,
            [
                call("amount_1250.png", confidence=0.80, timeout=10),
                call("continue_button.png", confidence=0.80, timeout=10),
                call("continue_button.png", confidence=0.80, timeout=10),
                call(
                    "payment_success.png",
                    confidence=0.80,
                    timeout=30,
                ),
            ],
        )
        wait_for_benefits_or_payment_mock.assert_called_once_with()
        handle_benefits_or_payment_mock.assert_called_once_with("payment")

    @patch("features.change_type_charge.click_image")
    def test_asset_click_falls_back_to_calibrated_coordinates(
        self,
        click_image_mock,
    ):
        click_image_mock.side_effect = [
            change_type_charge.ClickError("missing asset"),
            True,
        ]

        result = change_type_charge.click_asset_or_calibrated(
            "charge_type_amount_tab.png",
            timeout=10,
        )

        self.assertTrue(result)
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "charge_type_amount_tab.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "charge_type_amount_tab.png",
                    timeout=10,
                    use_coordinates=True,
                    use_region=False,
                ),
            ],
        )


if __name__ == "__main__":
    unittest.main()
