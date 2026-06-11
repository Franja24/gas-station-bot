import unittest
from types import SimpleNamespace
from unittest.mock import call, patch

from features import premium


class PremiumFlowTests(unittest.TestCase):
    @patch("features.premium.save_screenshot")
    @patch("features.premium.find_image")
    @patch("features.premium.click_image")
    @patch("features.premium.time.sleep")
    def test_clicks_no_benefits_when_prompt_is_visible(
        self,
        _sleep_mock,
        click_image_mock,
        find_image_mock,
        save_screenshot_mock,
    ):
        find_image_mock.return_value = SimpleNamespace(x=100, y=100)

        premium.handle_benefits_or_payment()

        click_image_mock.assert_called_once_with(
            "no_benefits_button.png",
            timeout=10,
            use_coordinates=False,
            use_region=False,
        )
        save_screenshot_mock.assert_called_once_with(
            "step_4_no_benefits_clicked"
        )

    @patch("features.premium.save_screenshot")
    @patch("features.premium.find_image")
    @patch("features.premium.click_image")
    @patch("features.premium.time.sleep")
    def test_skips_no_benefits_when_payment_is_already_visible(
        self,
        _sleep_mock,
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
                call("no_benefits_button.png", timeout=3),
                call("card.png", timeout=5),
            ],
        )
        save_screenshot_mock.assert_called_once_with(
            "step_4_no_benefits_skipped"
        )


if __name__ == "__main__":
    unittest.main()
