import unittest
from unittest.mock import call, patch

from features import confirm_transaction


class ConfirmTransactionTests(unittest.TestCase):
    @patch("features.confirm_transaction.time.sleep")
    @patch("features.confirm_transaction.save_screenshot")
    @patch("features.confirm_transaction.click_asset")
    @patch("features.confirm_transaction.assert_image_visible")
    @patch("features.confirm_transaction.open_settings_menu")
    @patch("features.confirm_transaction.open_anydesk")
    def test_confirms_latest_transaction_and_finishes_purchase(
        self,
        open_anydesk_mock,
        open_settings_menu_mock,
        assert_image_visible_mock,
        click_asset_mock,
        save_screenshot_mock,
        _sleep_mock,
    ):
        confirm_transaction.run()

        open_anydesk_mock.assert_called_once_with()
        open_settings_menu_mock.assert_called_once_with()
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
                    "confirm_transaction_modal_button.png",
                    confidence=0.80,
                    timeout=10,
                ),
                call("finalize_button.png", confidence=0.80, timeout=10),
            ],
        )
        self.assertEqual(
            click_asset_mock.call_args_list,
            [
                call("settings_transaction_log_option.png", timeout=10),
                call("transaction_log_first_row_marker.png", timeout=10),
                call("confirm_transaction_button.png", timeout=10),
                call("confirm_transaction_modal_button.png", timeout=10),
                call("finalize_button.png", timeout=10),
            ],
        )
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("step_1_settings_visible"),
                call("step_2_transaction_log_visible"),
                call("step_3_latest_transaction_visible"),
                call("step_4_confirm_transaction_clicked"),
                call("step_5_transaction_confirmed"),
                call("step_6_finalize_clicked"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
