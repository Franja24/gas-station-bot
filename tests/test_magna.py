import unittest
from unittest.mock import call, patch

from features import magna


class MagnaFlowTests(unittest.TestCase):
    @patch("features.magna.assert_image_visible")
    @patch("features.magna.save_screenshot")
    @patch("features.magna.click_image")
    @patch("features.magna.open_anydesk")
    def test_magna_completes_payment_without_no_benefits(
        self,
        open_anydesk_mock,
        click_image_mock,
        save_screenshot_mock,
        assert_image_visible_mock,
    ):
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
        self.assertNotIn(
            call("no_benefits_button.png", timeout=10),
            click_image_mock.call_args_list,
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call("amount_1250.png", confidence=0.80, timeout=10),
                call("continue_button.png", confidence=0.80, timeout=10),
                call("card.png", confidence=0.80, timeout=10),
                call(
                    "payment_success.png",
                    confidence=0.80,
                    timeout=30,
                ),
            ],
        )
        self.assertNotIn(
            call("step_4_no_benefits_clicked"),
            save_screenshot_mock.call_args_list,
        )


if __name__ == "__main__":
    unittest.main()
