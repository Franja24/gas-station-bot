import unittest
from types import SimpleNamespace
from unittest.mock import patch

import clicker
from config.regions import REGIONS
from config.settings import REFERENCE_SCREEN_SIZE


class ClickImageTests(unittest.TestCase):
    @patch("clicker.click_coordinates", return_value=True)
    @patch("clicker.find_image")
    def test_calibrated_target_skips_image_detection(
        self, find_image_mock, click_coordinates_mock
    ):
        result = clicker.click_image("premium.png")

        self.assertTrue(result)
        find_image_mock.assert_not_called()
        click_coordinates_mock.assert_called_once_with(640, 256)

    @patch("clicker.click_coordinates", return_value=True)
    @patch("clicker.find_image")
    def test_magna_uses_calibrated_green_button_coordinates(
        self, find_image_mock, click_coordinates_mock
    ):
        result = clicker.click_image("magna.png")

        self.assertTrue(result)
        find_image_mock.assert_not_called()
        click_coordinates_mock.assert_called_once_with(640, 398)

    @patch("clicker.click_coordinates", return_value=True)
    @patch("clicker.find_image")
    def test_sevenly_uses_calibrated_button_coordinates(
        self, find_image_mock, click_coordinates_mock
    ):
        result = clicker.click_image("sevenly.png")

        self.assertTrue(result)
        find_image_mock.assert_not_called()
        click_coordinates_mock.assert_called_once_with(718, 123)

    @patch("clicker.click_coordinates", return_value=True)
    @patch("clicker.find_image")
    def test_telefon_number_uses_calibrated_button_coordinates(
        self, find_image_mock, click_coordinates_mock
    ):
        result = clicker.click_image("telefon_number.png")

        self.assertTrue(result)
        find_image_mock.assert_not_called()
        click_coordinates_mock.assert_called_once_with(700, 385)

    @patch("clicker.click_coordinates", return_value=True)
    @patch("clicker.find_image")
    def test_uncalibrated_target_uses_safe_image_detection(
        self, find_image_mock, click_coordinates_mock
    ):
        find_image_mock.return_value = SimpleNamespace(x=1000, y=600)

        result = clicker.click_image("new_button.png", confidence=0.90)

        self.assertTrue(result)
        find_image_mock.assert_called_once()
        click_coordinates_mock.assert_called_once_with(500, 300)

    @patch("clicker.find_image", return_value=None)
    def test_missing_uncalibrated_target_stops_flow(self, _find_image_mock):
        with self.assertRaises(clicker.ClickError):
            clicker.click_image("new_button.png")

    @patch("clicker.find_image", return_value=SimpleNamespace(x=100, y=200))
    def test_visible_image_passes_functional_validation(self, find_image_mock):
        result = clicker.assert_image_visible("premium.png", timeout=15)

        self.assertTrue(result)
        find_image_mock.assert_called_once_with(
            "premium.png",
            confidence=0.80,
            timeout=15,
            region=None,
        )

    @patch("clicker.find_image", return_value=None)
    def test_missing_image_fails_functional_validation(self, _find_image_mock):
        with self.assertRaises(clicker.ClickError):
            clicker.assert_image_visible("premium.png", timeout=15)

    @patch("clicker.pyautogui.size", return_value=(1440, 900))
    def test_click_is_cancelled_when_screen_is_not_calibrated(self, _size_mock):
        with self.assertRaises(clicker.ClickError):
            clicker.click_coordinates(100, 100)

    def test_search_regions_stay_inside_calibrated_screen(self):
        screen_width, screen_height = REFERENCE_SCREEN_SIZE

        for image_name, (x, y, width, height) in REGIONS.items():
            with self.subTest(image_name=image_name):
                self.assertGreaterEqual(x, 0)
                self.assertGreaterEqual(y, 0)
                self.assertLessEqual(x + width, screen_width)
                self.assertLessEqual(y + height, screen_height)


if __name__ == "__main__":
    unittest.main()
