import unittest
from unittest.mock import call, patch

from features import return_to_product_selection


class ReturnToProductSelectionTests(unittest.TestCase):
    @patch("features.return_to_product_selection.save_screenshot")
    @patch("features.return_to_product_selection.time.sleep")
    @patch("features.return_to_product_selection.click_image")
    @patch("features.return_to_product_selection.find_image")
    @patch("features.return_to_product_selection.open_anydesk")
    def test_returns_from_declined_payment_screen_with_back_button(
        self,
        open_anydesk_mock,
        find_image_mock,
        click_image_mock,
        _sleep_mock,
        save_screenshot_mock,
    ):
        visible = object()
        find_image_mock.side_effect = [
            None,
            None,
            visible,
            visible,
            visible,
        ]

        return_to_product_selection.run()

        open_anydesk_mock.assert_called_once_with()
        click_image_mock.assert_called_once_with(
            "regresar_button.png",
            timeout=10,
            use_coordinates=False,
            use_region=False,
        )
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                call("return_to_product_selection_back_1"),
                call("product_selection_after_back"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
