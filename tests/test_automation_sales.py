import unittest
from unittest.mock import patch

from automation.flows.sales import start_amount_sale


class SalesFlowTests(unittest.TestCase):
    @patch("automation.flows.sales.run_amount_payment", return_value="approved")
    def test_parameterizes_product_amount_and_evidence_slug(self, run_mock):
        result = start_amount_sale(
            "Premium",
            200,
            require_payment_approval=True,
        )

        self.assertEqual(result, "approved")
        run_mock.assert_called_once_with(
            "200",
            "premium_amount_200",
            product="premium",
            require_payment_approval=True,
        )


if __name__ == "__main__":
    unittest.main()
