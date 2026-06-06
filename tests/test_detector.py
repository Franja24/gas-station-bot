import unittest
from types import SimpleNamespace
from unittest.mock import patch

import detector


class FindImageTests(unittest.TestCase):
    @patch("detector.time.sleep")
    @patch("detector.pyautogui.locateCenterOnScreen")
    def test_requires_two_safe_confirmations(self, locate_mock, _sleep_mock):
        location = SimpleNamespace(x=100, y=200)
        locate_mock.return_value = location

        result = detector.find_image(
            "login_button.png",
            confidence=0.25,
            timeout=1,
        )

        self.assertIs(result, location)
        self.assertEqual(locate_mock.call_count, 2)
        self.assertEqual(
            locate_mock.call_args.kwargs["confidence"],
            0.80,
        )

    @patch("detector.time.sleep")
    @patch("detector.pyautogui.locateCenterOnScreen")
    def test_unstable_match_is_not_confirmed(self, locate_mock, _sleep_mock):
        first = SimpleNamespace(x=100, y=200)
        second = SimpleNamespace(x=300, y=400)
        third = SimpleNamespace(x=303, y=404)
        locate_mock.side_effect = [first, second, third]

        result = detector.find_image("login_button.png", timeout=1)

        self.assertIs(result, third)
        self.assertEqual(locate_mock.call_count, 3)


if __name__ == "__main__":
    unittest.main()
