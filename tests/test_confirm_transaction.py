import unittest
from unittest.mock import call, patch

from features import confirm_transaction


class ConfirmTransactionTests(unittest.TestCase):
    @patch("features.confirm_transaction.click_transaction")
    @patch("features.confirm_transaction.find_image")
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
        find_image_mock,
        click_transaction_mock,
    ):
        find_image_mock.return_value = object()

        self.assertEqual(confirm_transaction.run(), "confirmed")

        open_anydesk_mock.assert_called_once_with()
        open_settings_menu_mock.assert_called_once_with()
        click_transaction_mock.assert_called_once_with(None)
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
            ],
        )
        self.assertEqual(
            click_asset_mock.call_args_list,
            [
                call("settings_transaction_log_option.png", timeout=10),
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

    @patch("features.confirm_transaction.click_transaction")
    @patch("features.confirm_transaction.find_image")
    @patch("features.confirm_transaction.save_screenshot")
    @patch("features.confirm_transaction.click_asset")
    @patch("features.confirm_transaction.assert_image_visible")
    @patch("features.confirm_transaction.open_settings_menu")
    @patch("features.confirm_transaction.open_anydesk")
    def test_returns_to_session_when_transaction_is_already_approved(
        self,
        open_anydesk_mock,
        open_settings_menu_mock,
        assert_image_visible_mock,
        click_asset_mock,
        save_screenshot_mock,
        find_image_mock,
        click_transaction_mock,
    ):
        find_image_mock.side_effect = [None, object()]

        self.assertEqual(confirm_transaction.run(expected_amount="200"), "already_approved")

        open_anydesk_mock.assert_called_once_with()
        open_settings_menu_mock.assert_called_once_with()
        click_transaction_mock.assert_called_once_with("200")
        self.assertEqual(
            find_image_mock.call_args_list[:2],
            [
                call("confirm_transaction_button.png", confidence=0.80, timeout=3),
                call("cancel_transaction_button.png", confidence=0.80, timeout=3),
            ],
        )
        self.assertEqual(
            click_asset_mock.call_args_list[-4:],
            [
                call("regresar_button.png", timeout=10),
                call("regresar_button.png", timeout=10),
                call("regresar_button.png", timeout=10),
                call("continue_session_button.png", timeout=10),
            ],
        )
        save_screenshot_mock.assert_any_call("step_4_transaction_already_approved")


if __name__ == "__main__":
    unittest.main()
