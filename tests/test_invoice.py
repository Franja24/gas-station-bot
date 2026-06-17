import sys
import types
import unittest
from unittest.mock import patch


applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("screenshot", screenshot_stub)

from features import invoice


class InvoiceFlowTests(unittest.TestCase):
    @patch("features.invoice.open_anydesk")
    @patch("features.invoice.time.sleep")
    @patch("features.invoice.save_screenshot")
    @patch("features.invoice.assert_image_visible")
    @patch("features.invoice.click_image")
    def test_uses_calibrated_coordinate_for_final_continue(
        self,
        click_image_mock,
        _assert_image_visible_mock,
        _save_screenshot_mock,
        _sleep_mock,
        _open_anydesk_mock,
    ):
        invoice.run()

        self.assertEqual(
            click_image_mock.call_args_list[-1],
            unittest.mock.call(
                "invoice_continue_button.png",
                timeout=10,
                use_coordinates=True,
                use_region=False,
            ),
        )


if __name__ == "__main__":
    unittest.main()
