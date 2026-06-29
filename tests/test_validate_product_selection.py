import unittest
from unittest.mock import call, patch

from features import validate_product_selection


class ValidateProductSelectionTests(unittest.TestCase):
    @patch("features.validate_product_selection.save_screenshot")
    @patch("features.validate_product_selection.assert_image_visible")
    @patch("features.validate_product_selection.open_anydesk")
    def test_validates_premium_and_magna_are_visible(
        self,
        open_anydesk_mock,
        assert_image_visible_mock,
        save_screenshot_mock,
    ):
        validate_product_selection.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call("premium.png", confidence=0.80, timeout=10),
                call("magna.png", confidence=0.80, timeout=10),
            ],
        )
        save_screenshot_mock.assert_called_once_with(
            "product_selection_premium_magna_visible"
        )


if __name__ == "__main__":
    unittest.main()
