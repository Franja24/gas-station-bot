import sys
import types
import unittest
from unittest.mock import call, patch


detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: None

login_stub = types.ModuleType("features.login")
login_stub.run = lambda: None

manual_cancel_stub = types.ModuleType(
    "features.manual_cancel_last_transation"
)
manual_cancel_stub.run = lambda: None

out_of_service_stub = types.ModuleType("features.out_of_service")
out_of_service_stub.is_out_of_service_visible = lambda *args, **kwargs: False

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("detector", detector_stub)
sys.modules.setdefault("features.login", login_stub)
sys.modules.setdefault(
    "features.manual_cancel_last_transation",
    manual_cancel_stub,
)
sys.modules.setdefault("features.out_of_service", out_of_service_stub)
sys.modules.setdefault("screenshot", screenshot_stub)

from features import login_if_needed


class LoginIfNeededTests(unittest.TestCase):
    @patch("features.login_if_needed.save_screenshot")
    @patch("features.login_if_needed.login_run")
    @patch("features.login_if_needed.find_image", return_value=object())
    def test_skips_login_when_premium_is_visible(
        self,
        find_image_mock,
        login_run_mock,
        save_screenshot_mock,
    ):
        login_if_needed.run()

        find_image_mock.assert_called_once_with("premium.png", timeout=3)
        login_run_mock.assert_not_called()
        save_screenshot_mock.assert_called_once_with(
            "premium_visible_skip_login"
        )

    @patch("features.login_if_needed.save_screenshot")
    @patch("features.login_if_needed.login_run")
    @patch("features.login_if_needed.find_image", return_value=None)
    def test_runs_login_when_premium_is_not_visible(
        self,
        _find_image_mock,
        login_run_mock,
        save_screenshot_mock,
    ):
        login_if_needed.run()

        login_run_mock.assert_called_once_with()
        save_screenshot_mock.assert_not_called()

    @patch("features.login_if_needed.save_screenshot")
    @patch("features.login_if_needed.manual_cancel_last_transation_run")
    @patch("features.login_if_needed.is_out_of_service_visible")
    @patch("features.login_if_needed.login_run")
    @patch("features.login_if_needed.find_image")
    def test_cancels_last_transaction_when_pump_is_out_of_service(
        self,
        find_image_mock,
        login_run_mock,
        is_out_of_service_visible_mock,
        manual_cancel_last_transation_run_mock,
        save_screenshot_mock,
    ):
        find_image_mock.return_value = None
        is_out_of_service_visible_mock.return_value = True
        login_run_mock.side_effect = [RuntimeError("no premium"), None]

        login_if_needed.run()

        find_image_mock.assert_called_once_with("premium.png", timeout=3)
        is_out_of_service_visible_mock.assert_called_once_with(timeout=3)
        self.assertEqual(login_run_mock.call_count, 2)
        manual_cancel_last_transation_run_mock.assert_called_once_with()
        save_screenshot_mock.assert_called_once_with(
            "pump_out_of_service_detected"
        )


if __name__ == "__main__":
    unittest.main()
