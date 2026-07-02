import unittest
from types import SimpleNamespace
from unittest.mock import call, patch

from clicker import ClickError
from features import charge_operation


class ChargeOperationTests(unittest.TestCase):
    @patch("features.charge_operation.run_stages")
    def test_runs_three_stage_groups_without_sevenly(self, run_stages_mock):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = charge_operation.run(
            product="premium",
            charge_type="amount_500",
        )

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "00_prepare_product_selection",
                "02_select_product",
                "03_select_charge",
                "04_complete_card_payment",
                "05_windows_app_and_finalize",
            ],
        )

    @patch("features.charge_operation.run_stages")
    def test_includes_sevenly_login_when_enabled(self, run_stages_mock):
        charge_operation.run(
            product="magna",
            charge_type="liters_20",
            use_sevenly=True,
        )

        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "00_prepare_product_selection",
                "01_sevenly_login",
                "02_select_product",
                "03_select_charge",
                "04_complete_card_payment",
                "05_windows_app_and_finalize",
            ],
        )

    @patch("features.charge_operation.save_screenshot")
    @patch("features.charge_operation.assert_image_visible")
    @patch("features.charge_operation.time.sleep")
    @patch("features.charge_operation.click_image")
    def test_selects_amount_500_with_existing_change_type_pattern(
        self,
        click_image_mock,
        _sleep_mock,
        assert_image_visible_mock,
        _save_screenshot_mock,
    ):
        charge_operation.select_charge("amount_500")

        self.assertEqual(
            click_image_mock.call_args_list,
            [
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
            ],
        )
        assert_image_visible_mock.assert_called_once_with(
            "continue_button.png",
            confidence=0.80,
            timeout=10,
        )

    @patch("features.charge_operation.save_screenshot")
    @patch("features.charge_operation.assert_image_visible")
    @patch("features.charge_operation.time.sleep")
    @patch("features.charge_operation.click_image")
    def test_liters_20_falls_back_to_calibrated_coordinates(
        self,
        click_image_mock,
        _sleep_mock,
        assert_image_visible_mock,
        _save_screenshot_mock,
    ):
        click_image_mock.side_effect = [
            True,
            ClickError("missing asset"),
            True,
            ClickError("missing asset"),
            True,
        ]

        charge_operation.select_charge("liters_20")

        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "amount_1250.png",
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
                    "charge_type_liters_tab.png",
                    timeout=10,
                    use_coordinates=True,
                    use_region=False,
                ),
                call(
                    "charge_liters_20.png",
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
            ],
        )
        assert_image_visible_mock.assert_called_once_with(
            "continue_button.png",
            confidence=0.80,
            timeout=10,
        )

    @patch("features.charge_operation.save_screenshot")
    @patch("features.charge_operation.assert_image_visible")
    @patch("features.charge_operation.time.sleep")
    @patch("features.charge_operation.click_image")
    @patch("features.charge_operation.find_image")
    @patch("features.charge_operation.open_anydesk")
    def test_select_product_uses_detected_asset_before_calibrated_coordinates(
        self,
        open_anydesk_mock,
        find_image_mock,
        click_image_mock,
        _sleep_mock,
        assert_image_visible_mock,
        save_screenshot_mock,
    ):
        find_image_mock.side_effect = [
            None,
            None,
            SimpleNamespace(x=1493, y=596),
        ]

        charge_operation.select_product("magna")

        open_anydesk_mock.assert_called_once_with()
        assert_image_visible_mock.assert_any_call(
            "magna.png",
            confidence=0.80,
            timeout=20,
        )
        click_image_mock.assert_called_once_with(
            "magna.png",
            timeout=5,
            use_coordinates=False,
            use_region=False,
        )
        save_screenshot_mock.assert_called_once_with(
            "charge_operation_magna_selected"
        )


if __name__ == "__main__":
    unittest.main()
