import unittest
from unittest.mock import patch

from features import sevenly_e2e


class SevenlyE2EFlowTests(unittest.TestCase):
    @patch("features.sevenly_e2e.invoice_run")
    @patch("features.sevenly_e2e.windows_run")
    @patch("features.sevenly_e2e.magna_run")
    @patch("features.sevenly_e2e.sevenly_login_run")
    @patch("features.sevenly_e2e.login_run")
    def test_runs_sevenly_magna_flow_in_order(
        self,
        login_mock,
        sevenly_login_mock,
        magna_mock,
        windows_mock,
        invoice_mock,
    ):
        calls = []

        login_mock.side_effect = lambda: calls.append("login")
        sevenly_login_mock.side_effect = lambda: calls.append("sevenly_login")
        magna_mock.side_effect = lambda: calls.append("magna")
        windows_mock.side_effect = lambda: calls.append("windows")
        invoice_mock.side_effect = lambda: calls.append("invoice")

        sevenly_e2e.run()

        self.assertEqual(
            calls,
            [
                "login",
                "sevenly_login",
                "magna",
                "windows",
                "invoice",
            ],
        )


if __name__ == "__main__":
    unittest.main()
