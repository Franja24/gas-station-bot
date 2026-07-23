import unittest
from types import SimpleNamespace
from unittest.mock import call, patch

from features import payment_declined_response


class PaymentDeclinedResponseTests(unittest.TestCase):
    @patch(
        "features.payment_declined_response.declined_response_table_region",
        return_value=(1050, 300, 200, 150),
    )
    @patch("features.payment_declined_response.click_image")
    def test_clicks_response_eye_from_declined_row(
        self,
        click_image_mock,
        _region_mock,
    ):
        payment_declined_response.click_declined_response_eye()

        click_image_mock.assert_called_once_with(
            "declined_response_eye_button.png",
            timeout=10,
            use_coordinates=False,
            use_region=False,
            region=(1050, 300, 200, 150),
        )

    @patch(
        "features.payment_declined_response"
        ".return_to_product_selection_after_log_review"
    )
    @patch("features.payment_declined_response.save_screenshot")
    @patch("features.payment_declined_response.click_declined_response_eye")
    @patch("features.payment_declined_response.open_settings_menu")
    @patch("features.payment_declined_response.click_asset")
    @patch("features.payment_declined_response.assert_image_visible")
    @patch("features.payment_declined_response.open_anydesk")
    def test_validates_declined_payment_response(
        self,
        open_anydesk_mock,
        assert_image_visible_mock,
        click_asset_mock,
        open_settings_menu_mock,
        click_declined_response_eye_mock,
        save_screenshot_mock,
        return_after_review_mock,
    ):
        payment_declined_response.run()

        open_anydesk_mock.assert_called_once_with()
        open_settings_menu_mock.assert_called_once_with()
        click_declined_response_eye_mock.assert_called_once_with()
        return_after_review_mock.assert_called_once_with()
        self.assertEqual(
            click_asset_mock.call_args_list,
            [
                call("regresar_button.png", timeout=10),
                call("settings_transaction_log_option.png", timeout=10),
                call("transaction_log_first_row_marker.png", timeout=10),
            ],
        )
        self.assertIn(
            call(
                "metadata_response_title.png",
                confidence=0.80,
                timeout=10,
            ),
            assert_image_visible_mock.call_args_list,
        )
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("declined_step_1_payment_declined_visible"),
                call("declined_step_2_product_selection_visible"),
                call("declined_step_3_settings_visible"),
                call("declined_step_4_transaction_log_visible"),
                call("declined_step_5_latest_declined_transaction_visible"),
                call("declined_step_6_response_metadata_visible"),
            ],
        )

    @patch("features.payment_declined_response.find_image")
    def test_accepts_start_screen_after_log_review(self, find_image_mock):
        find_image_mock.side_effect = [
            None,
            SimpleNamespace(x=960, y=718),
        ]

        self.assertEqual(
            payment_declined_response.wait_for_restored_kiosk_state(),
            "start",
        )

    @patch("features.payment_declined_response.find_image")
    def test_accepts_product_selection_after_log_review(self, find_image_mock):
        find_image_mock.side_effect = [
            SimpleNamespace(x=960, y=388),
            SimpleNamespace(x=960, y=580),
        ]

        self.assertEqual(
            payment_declined_response.wait_for_restored_kiosk_state(),
            "product_selection",
        )


if __name__ == "__main__":
    unittest.main()
