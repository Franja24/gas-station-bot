import unittest
from unittest.mock import call, patch

from features import sevenly_login_error


class SevenlyLoginErrorFlowTests(unittest.TestCase):
    @patch("features.sevenly_login_error.assert_image_visible")
    @patch("features.sevenly_login_error.save_screenshot")
    @patch("features.sevenly_login_error.click_image")
    @patch("features.sevenly_login_error.time.sleep")
    @patch("features.sevenly_login_error.open_anydesk")
    def test_sevenly_login_error_validates_error_message(
        self,
        open_anydesk_mock,
        _sleep_mock,
        click_image_mock,
        save_screenshot_mock,
        assert_image_visible_mock,
    ):
        sevenly_login_error.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call("sevenly.png", timeout=10),
                call("telefon_number.png", timeout=10),
                call("five_button.png", timeout=10),
                call("five_button.png", timeout=10),
                call("three_button.png", timeout=10),
                call("one_button.png", timeout=10),
                call("zero_button.png", timeout=10),
                call("four_button.png", timeout=10),
                call("four_button.png", timeout=10),
                call("eight_button.png", timeout=10),
                call("four_button.png", timeout=10),
                call("zero_button.png", timeout=10),
                call("continue_button.png", timeout=10),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call(
                    "no_registered_benefits_number.png",
                    confidence=0.80,
                    timeout=15,
                ),
                call(
                    "sevenly.png",
                    confidence=0.80,
                    timeout=15,
                    region=sevenly_login_error.SEVENLY_GREETING_REGION,
                ),
            ],
        )
        save_screenshot_mock.assert_called_with(
            "step_5_error_message_visible"
        )


if __name__ == "__main__":
    unittest.main()
