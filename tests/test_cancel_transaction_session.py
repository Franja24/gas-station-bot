import sys
import types
import unittest
from unittest.mock import call, patch

clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

kiosk_process_stub = types.ModuleType("features.kiosk_process")
kiosk_process_stub.force_close_kiosk_process = lambda: None

manual_cancel_stub = types.ModuleType("features.manual_cancel_last_transation")
manual_cancel_stub.click_asset = lambda *args, **kwargs: True
manual_cancel_stub.open_settings_menu = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("features.kiosk_process", kiosk_process_stub)
sys.modules.setdefault(
    "features.manual_cancel_last_transation",
    manual_cancel_stub,
)
sys.modules.setdefault("screenshot", screenshot_stub)

from features import cancel_transaction_session


class CancelTransactionSessionTests(unittest.TestCase):
    @patch("features.cancel_transaction_session.time.sleep")
    @patch("features.cancel_transaction_session.force_close_kiosk_process")
    @patch("features.cancel_transaction_session.save_screenshot")
    @patch("features.cancel_transaction_session.click_asset")
    @patch("features.cancel_transaction_session.assert_image_visible")
    @patch("features.cancel_transaction_session.open_settings_menu")
    @patch("features.cancel_transaction_session.open_anydesk")
    def test_cancels_latest_transaction_and_leaves_kiosk_clean(
        self,
        open_anydesk_mock,
        open_settings_menu_mock,
        assert_image_visible_mock,
        click_asset_mock,
        save_screenshot_mock,
        force_close_kiosk_process_mock,
        _sleep_mock,
    ):
        cancel_transaction_session.run()

        open_anydesk_mock.assert_called_once_with()
        open_settings_menu_mock.assert_called_once_with()
        force_close_kiosk_process_mock.assert_called_once_with()
        self.assertEqual(
            click_asset_mock.call_args_list,
            [
                call("settings_transaction_log_option.png", timeout=10),
                call("transaction_log_first_row_marker.png", timeout=10),
                call("cancel_transaction_button.png", timeout=10),
                call("confirm_cancel_transaction_button.png", timeout=10),
                call("regresar_button.png", timeout=10),
                call("regresar_button.png", timeout=10),
                call("continue_session_button.png", timeout=10),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call(
                    "pump_out_of_service_title.png",
                    confidence=0.80,
                    timeout=10,
                ),
                call(
                    "pump_out_of_service_icon.png",
                    confidence=0.80,
                    timeout=10,
                ),
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
                call(
                    "transaction_log_title.png",
                    confidence=0.80,
                    timeout=10,
                ),
                call(
                    "continue_session_button.png",
                    confidence=0.80,
                    timeout=10,
                ),
                call("premium.png", confidence=0.80, timeout=10),
                call("magna.png", confidence=0.80, timeout=10),
            ],
        )
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("step_1_pump_out_of_service_visible"),
                call("step_2_settings_visible"),
                call("step_3_transaction_log_visible"),
                call("step_4_latest_transaction_visible"),
                call("step_5_cancel_transaction_clicked"),
                call("step_6_cancel_transaction_confirmed"),
                call("step_7_back_to_transaction_log"),
                call("step_8_back_to_settings"),
                call("step_9_product_selection_visible"),
                call("step_10_kiosk_process_force_close"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
