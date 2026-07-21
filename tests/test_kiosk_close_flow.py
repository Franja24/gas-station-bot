import unittest
from unittest.mock import patch

from automation.flows.kiosk_close import KioskCloseFlow


class KioskCloseFlowTests(unittest.TestCase):
    @patch("automation.flows.kiosk_close.start_amount_sale", return_value="approved")
    def test_keeps_payment_result_by_product_and_amount(self, start_sale_mock):
        flow = KioskCloseFlow()

        self.assertEqual(
            flow.start_sale("Magna", 150, require_approval=True),
            "approved",
        )
        flow.require_approved_payment("Magna", 150)

        start_sale_mock.assert_called_once_with(
            "Magna",
            150,
            require_payment_approval=True,
        )

    @patch("automation.flows.kiosk_close.transactions.cancel_transaction")
    def test_cancels_expected_amount_without_closing_kiosk(self, cancel_mock):
        flow = KioskCloseFlow()

        flow.cancel_transaction(150)

        cancel_mock.assert_called_once_with(
            force_close_after=False,
            expected_amount="150",
        )

    @patch("automation.flows.kiosk_close.transactions.confirm_transaction")
    def test_confirms_expected_amount(self, confirm_mock):
        flow = KioskCloseFlow()

        flow.confirm_transaction(200)

        confirm_mock.assert_called_once_with(expected_amount="200")


if __name__ == "__main__":
    unittest.main()
