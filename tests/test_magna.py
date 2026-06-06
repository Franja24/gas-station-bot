import unittest
from unittest.mock import call, patch

from features import magna


class MagnaFlowTests(unittest.TestCase):
    @patch("features.magna.assert_image_visible")
    @patch("features.magna.save_screenshot")
    @patch("features.magna.click_image")
    @patch("features.magna.time.sleep")
    @patch("features.magna.open_anydesk")
    def test_magna_completes_payment_without_no_benefits(
        self,
        open_anydesk_mock,
        _sleep_mock,
        click_image_mock,
        save_screenshot_mock,
        assert_image_visible_mock,
    ):
        magna.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call("magna.png", timeout=10),
                call("amount_1250.png", timeout=10),
                call("continue_button.png", timeout=10),
                call("card.png", timeout=10),
            ],
        )
        self.assertNotIn(
            call("no_benefits_button.png", timeout=10),
            click_image_mock.call_args_list,
        )
        assert_image_visible_mock.assert_called_once_with(
            "payment_success.png",
            confidence=0.80,
            timeout=15,
        )
        self.assertNotIn(
            call("step_4_no_benefits_clicked"),
            save_screenshot_mock.call_args_list,
        )


if __name__ == "__main__":
    unittest.main()
