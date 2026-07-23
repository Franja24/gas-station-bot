import unittest
from unittest.mock import call, patch

from features import magna


class MagnaFlowTests(unittest.TestCase):
    @patch("features.magna.handle_payment_result")
    @patch(
        "features.magna.wait_for_payment_result",
        return_value="ready_for_dispatch",
    )
    @patch("features.magna.handle_benefits_or_payment")
    @patch("features.magna.wait_for_benefits_or_payment")
    @patch("features.magna.assert_image_visible")
    @patch("features.magna.save_screenshot")
    @patch("features.magna.click_image")
    @patch("features.magna.open_anydesk")
    def test_magna_completes_payment_after_benefits_resolution(
        self,
        open_anydesk_mock,
        click_image_mock,
        save_screenshot_mock,
        assert_image_visible_mock,
        wait_for_benefits_or_payment_mock,
        handle_benefits_or_payment_mock,
        wait_for_payment_result_mock,
        handle_payment_result_mock,
    ):
        wait_for_benefits_or_payment_mock.return_value = "no_benefits"

        magna.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "magna.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "amount_1250.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "continue_button.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "card.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call("amount_1250.png", confidence=0.80, timeout=10),
                call("continue_button.png", confidence=0.80, timeout=10),
            ],
        )
        self.assertNotIn(
            call("step_4_no_benefits_clicked"),
            save_screenshot_mock.call_args_list,
        )
        wait_for_benefits_or_payment_mock.assert_called_once_with()
        handle_benefits_or_payment_mock.assert_called_once_with("no_benefits")
        wait_for_payment_result_mock.assert_called_once_with(timeout=30)
        handle_payment_result_mock.assert_called_once_with("ready_for_dispatch")


if __name__ == "__main__":
    unittest.main()
