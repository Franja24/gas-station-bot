import unittest
from unittest.mock import call, patch

from features import payment_declined_response


class PaymentDeclinedResponseTests(unittest.TestCase):
    @patch("features.payment_declined_response.click_image")
    def test_clicks_response_eye_from_declined_row(
        self,
        click_image_mock,
    ):
        payment_declined_response.click_declined_response_eye()

        click_image_mock.assert_called_once_with(
            "declined_response_eye_button.png",
            timeout=10,
            use_coordinates=False,
            use_region=False,
            region=payment_declined_response.DECLINED_RESPONSE_TABLE_REGION,
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
    ):
        payment_declined_response.run()

        open_anydesk_mock.assert_called_once_with()
        open_settings_menu_mock.assert_called_once_with()
        click_declined_response_eye_mock.assert_called_once_with()
        self.assertEqual(
            click_asset_mock.call_args_list,
            [
                call("regresar_button.png", timeout=10),
                call("settings_transaction_log_option.png", timeout=10),
                call("transaction_log_first_row_marker.png", timeout=10),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call(
                    "payment_declined_title.png",
                    confidence=0.80,
                    timeout=10,
                ),
                call("premium.png", confidence=0.80, timeout=10),
                call("magna.png", confidence=0.80, timeout=10),
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
                    "declined_response_eye_button.png",
                    confidence=0.80,
                    timeout=10,
                    region=(
                        payment_declined_response
                        .DECLINED_RESPONSE_TABLE_REGION
                    ),
                ),
                call(
                    "metadata_response_title.png",
                    confidence=0.80,
                    timeout=10,
                ),
            ],
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


if __name__ == "__main__":
    unittest.main()
