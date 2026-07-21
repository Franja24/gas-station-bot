import unittest
from types import SimpleNamespace
from unittest.mock import call, patch

from clicker import ClickError
from features import premium


class PremiumFlowTests(unittest.TestCase):
    @patch("features.premium.assert_image_visible")
    @patch("features.premium.save_screenshot")
    @patch("features.premium.find_image")
    @patch("features.premium.click_image")
    def test_clicks_no_benefits_when_prompt_is_visible(
        self,
        click_image_mock,
        find_image_mock,
        save_screenshot_mock,
        assert_image_visible_mock,
    ):
        find_image_mock.return_value = SimpleNamespace(x=100, y=100)

        premium.handle_benefits_or_payment()

        click_image_mock.assert_called_once_with(
            "no_benefits_button.png",
            timeout=10,
            use_coordinates=False,
            use_region=False,
        )
        assert_image_visible_mock.assert_called_once_with(
            "card.png",
            confidence=0.80,
            timeout=premium.PAYMENT_SCREEN_TIMEOUT_SECONDS,
        )
        save_screenshot_mock.assert_called_once_with(
            "step_4_no_benefits_clicked"
        )

    @patch("features.premium.save_screenshot")
    @patch("features.premium.find_image")
    @patch("features.premium.click_image")
    def test_skips_no_benefits_when_payment_is_already_visible(
        self,
        click_image_mock,
        find_image_mock,
        save_screenshot_mock,
    ):
        find_image_mock.side_effect = [
            None,
            SimpleNamespace(x=100, y=100),
        ]

        premium.handle_benefits_or_payment()

        click_image_mock.assert_not_called()
        self.assertEqual(
            find_image_mock.call_args_list,
            [
                call("no_benefits_button.png", timeout=1),
                call("card.png", timeout=1),
            ],
        )
        save_screenshot_mock.assert_called_once_with(
            "step_4_no_benefits_skipped"
        )

    @patch("features.premium.find_image")
    def test_wait_for_payment_result_detects_success(self, find_image_mock):
        find_image_mock.return_value = SimpleNamespace(x=100, y=100)

        self.assertEqual(premium.wait_for_payment_result(), "success")

        find_image_mock.assert_called_once_with(
            "payment_success.png",
            timeout=1,
        )

    @patch("features.premium.find_image")
    def test_wait_for_payment_result_detects_declined(self, find_image_mock):
        find_image_mock.side_effect = [
            None,
            SimpleNamespace(x=100, y=100),
        ]

        self.assertEqual(premium.wait_for_payment_result(), "declined")

        self.assertEqual(
            find_image_mock.call_args_list,
            [
                call("payment_success.png", timeout=1),
                call("payment_declined_title.png", timeout=1),
            ],
        )

    @patch("features.premium.save_screenshot")
    def test_handle_payment_result_keeps_success_flow(
        self,
        save_screenshot_mock,
    ):
        premium.handle_payment_result("success")

        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("step_5.1_complete_payment"),
                call("step_6_payment_success"),
                call("instructions pumb server"),
            ],
        )

    @patch("features.premium.payment_declined_response_run")
    def test_handle_payment_result_validates_declined_response_and_fails_case(
        self,
        payment_declined_response_run_mock,
    ):
        with self.assertRaisesRegex(
            ClickError,
            "Pago declinado; se validó la metadata",
        ):
            premium.handle_payment_result("declined")

        payment_declined_response_run_mock.assert_called_once_with(open_app=False)


if __name__ == "__main__":
    unittest.main()
