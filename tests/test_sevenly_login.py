import unittest
from pathlib import Path
from types import SimpleNamespace
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
    @patch("features.sevenly_login.click_coordinates")
    @patch("features.sevenly_login.find_image")
    @patch("features.sevenly_login.click_image")
    @patch("features.sevenly_login.time.sleep")
    @patch("features.sevenly_login.open_anydesk")
    def test_sevenly_login_enters_phone_and_validates_greeting(
        self,
        open_anydesk_mock,
        _sleep_mock,
        click_image_mock,
        find_image_mock,
        click_coordinates_mock,
        save_screenshot_mock,
        assert_image_visible_mock,
    ):
        find_image_mock.side_effect = [
            None,
            None,
            SimpleNamespace(x=1280, y=430),
        ]

        sevenly_login.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "sevenly.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "telefon_number.png",
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
            ],
        )
        self.assertEqual(click_coordinates_mock.call_count, 10)
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

    @patch("features.sevenly_login.save_screenshot")
    @patch("features.sevenly_login.find_image")
    @patch("features.sevenly_login.click_image")
    @patch("features.sevenly_login.time.sleep")
    @patch("features.sevenly_login.open_anydesk")
    def test_sevenly_login_skips_phone_when_customer_already_logged_in(
        self,
        open_anydesk_mock,
        _sleep_mock,
        click_image_mock,
        find_image_mock,
        save_screenshot_mock,
    ):
        find_image_mock.return_value = SimpleNamespace(x=1250, y=250)

        sevenly_login.run()

        open_anydesk_mock.assert_called_once_with()
        click_image_mock.assert_not_called()
        save_screenshot_mock.assert_called_once_with(
            "step_0_sevenly_already_logged_in"
        )

    @patch("features.sevenly_login.assert_image_visible")
    @patch("features.sevenly_login.save_screenshot")
    @patch("features.sevenly_login.click_coordinates")
    @patch("features.sevenly_login.find_image")
    @patch("features.sevenly_login.click_image")
    @patch("features.sevenly_login.time.sleep")
    @patch("features.sevenly_login.open_anydesk")
    def test_sevenly_login_continues_when_phone_is_cached(
        self,
        _open_anydesk_mock,
        _sleep_mock,
        click_image_mock,
        find_image_mock,
        click_coordinates_mock,
        save_screenshot_mock,
        _assert_image_visible_mock,
    ):
        find_image_mock.side_effect = [
            None,
            None,
            None,
            SimpleNamespace(x=1280, y=430),
        ]

        sevenly_login.run()

        click_coordinates_mock.assert_not_called()
        self.assertIn(
            call("step_3_phone_number_already_entered"),
            save_screenshot_mock.call_args_list,
        )
        self.assertEqual(
            click_image_mock.call_args_list[-1],
            call(
                "continue_button.png",
                timeout=10,
                use_coordinates=False,
                use_region=False,
            ),
        )


if __name__ == "__main__":
    unittest.main()
