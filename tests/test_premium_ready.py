import unittest
from unittest.mock import patch

from features import premium_ready


class PremiumReadyTests(unittest.TestCase):
    @patch("features.premium_ready.premium_run")
    @patch("features.premium_ready.prepare_product_selection")
    def test_reopens_kiosk_before_premium(
        self,
        prepare_product_selection_mock,
        premium_run_mock,
    ):
        premium_run_mock.return_value = {"stages": []}

        result = premium_ready.run()

        prepare_product_selection_mock.assert_called_once_with()
        premium_run_mock.assert_called_once_with()
        self.assertEqual(result, {"stages": []})


if __name__ == "__main__":
    unittest.main()
