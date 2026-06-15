import unittest
from types import SimpleNamespace
from unittest.mock import call, patch

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
            timeout=10,
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


if __name__ == "__main__":
    unittest.main()
