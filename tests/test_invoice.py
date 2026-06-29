import sys
import types
import unittest
from unittest.mock import patch


clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: None

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("detector", detector_stub)
sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("screenshot", screenshot_stub)

from features import invoice


class InvoiceTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
