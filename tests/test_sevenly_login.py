import unittest
from pathlib import Path
from unittest.mock import call, patch

from PIL import Image

from features import sevenly_login


class SevenlyLoginFlowTests(unittest.TestCase):
    def test_greeting_region_is_large_enough_for_sevenly_asset(self):
        asset_path = (
            Path(sevenly_login.__file__).resolve().parents[1]
            / "assets"
            / "sevenly.png"
        )
        region_width = sevenly_login.SEVENLY_GREETING_REGION[2]
        region_height = sevenly_login.SEVENLY_GREETING_REGION[3]

        with Image.open(asset_path) as asset:
            asset_width, asset_height = asset.size

        self.assertGreaterEqual(region_width, asset_width)
        self.assertGreaterEqual(region_height, asset_height)

    @patch("features.sevenly_login.assert_image_visible")
    @patch("features.sevenly_login.save_screenshot")
    @patch("features.sevenly_login.click_image")
    @patch("features.sevenly_login.time.sleep")
    @patch("features.sevenly_login.open_anydesk")
    def test_sevenly_login_enters_phone_and_validates_greeting(
        self,
        open_anydesk_mock,
        _sleep_mock,
        click_image_mock,
        save_screenshot_mock,
        assert_image_visible_mock,
    ):
        sevenly_login.run()

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
                call("one_button.png", timeout=10),
                call("continue_button.png", timeout=10),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call("premium.png", confidence=0.80, timeout=15),
                call(
                    "sevenly.png",
                    confidence=0.80,
                    timeout=15,
                    region=sevenly_login.SEVENLY_GREETING_REGION,
                ),
            ],
        )
        save_screenshot_mock.assert_called_with(
            "step_5_hola_cliente_visible"
        )


if __name__ == "__main__":
    unittest.main()
