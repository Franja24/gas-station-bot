import unittest
from unittest.mock import patch

from features import declined_transaction_e2e


class DeclinedTransactionE2eFlowTests(unittest.TestCase):
    @patch("features.declined_transaction_e2e.run_stages")
    def test_runs_declined_transaction_e2e_flow_as_reportable_stages(
        self,
        run_stages_mock,
    ):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = declined_transaction_e2e.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "01_prepare_product_selection",
                "02_create_magna_payment",
                "03_route_payment_result",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                declined_transaction_e2e.prepare_product_selection,
                declined_transaction_e2e.create_magna_payment,
                declined_transaction_e2e.route_payment_result,
            ],
        )


if __name__ == "__main__":
    unittest.main()
