import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import call, patch


clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: None

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

print_stub = types.ModuleType("features.print")
print_stub.run = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("detector", detector_stub)
sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("features.print", print_stub)
sys.modules.setdefault("screenshot", screenshot_stub)

from features import invoice


class InvoiceFlowTests(unittest.TestCase):
    @patch("features.invoice.save_screenshot")
    @patch("features.invoice.assert_image_visible")
    @patch("features.invoice.click_asset")
    @patch("features.invoice.is_visible")
    @patch("features.invoice.open_anydesk")
    def test_cancels_invoice_when_stuck_on_billing_info(
        self,
        open_anydesk_mock,
        is_visible_mock,
        click_asset_mock,
        assert_image_visible_mock,
        save_screenshot_mock,
    ):
        is_visible_mock.return_value = True

        invoice.run()

        open_anydesk_mock.assert_called_once_with()
        click_asset_mock.assert_called_once_with(
            "cancel_invoice_button.png",
            timeout=10,
        )
        assert_image_visible_mock.assert_called_once_with(
            "print_ticket_button.png",
            confidence=0.80,
            timeout=10,
        )
        save_screenshot_mock.assert_called_once_with(
            "invoice_cancelled_back_to_summary"
        )

    @patch("features.invoice.open_anydesk")
    @patch("features.invoice.time.sleep")
    @patch("features.invoice.save_screenshot")
    @patch("features.invoice.assert_image_visible")
    @patch("features.invoice.click_image")
    @patch("features.invoice.find_image")
    def test_uses_calibrated_coordinate_for_final_continue(
        self,
        find_image_mock,
        click_image_mock,
        _assert_image_visible_mock,
        _save_screenshot_mock,
        _sleep_mock,
        _open_anydesk_mock,
    ):
        find_image_mock.side_effect = [
            None,
            SimpleNamespace(),
            SimpleNamespace(),
            SimpleNamespace(),
        ]

        invoice.run()

        self.assertEqual(
            click_image_mock.call_args_list[-1],
            call(
                "invoice_continue_button.png",
                timeout=10,
                use_coordinates=True,
                use_region=False,
            ),
        )


if __name__ == "__main__":
    unittest.main()
