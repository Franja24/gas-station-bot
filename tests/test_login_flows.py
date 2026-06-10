import unittest
from unittest.mock import call, patch

from features import login, login_error


class LoginFlowTests(unittest.TestCase):
    @patch("features.login.assert_image_visible")
    @patch("features.login.save_screenshot")
    @patch("features.login.click_coordinates")
    @patch("features.login.click_image")
    @patch("features.login.time.sleep")
    @patch("features.login.open_anydesk")
    def test_login_uses_configurable_id_and_password(
        self,
        open_anydesk_mock,
        _sleep_mock,
        click_image_mock,
        click_coordinates_mock,
        _save_screenshot_mock,
        assert_image_visible_mock,
    ):
        login.run()

        open_anydesk_mock.assert_called_once_with()
        click_coordinates_mock.assert_called_once_with(660, 310)
        self.assertEqual(
            click_image_mock.call_args_list[:8],
            [
                call("login_button.png"),
                call("login_two_button.png", timeout=10),
                call("login_one_button.png", timeout=10),
                call("login_two_button.png", timeout=10),
                call("login_three_button.png", timeout=10),
                call("login_four_button.png", timeout=10),
                call("login_five_button.png", timeout=10),
                call("login_six_button.png", timeout=10),
            ],
        )
        assert_image_visible_mock.assert_called_once_with(
            "premium.png",
            confidence=0.80,
            timeout=15,
        )

    @patch("features.login_error.assert_image_visible")
    @patch("features.login_error.save_screenshot")
    @patch("features.login_error.click_coordinates")
    @patch("features.login_error.click_image")
    @patch("features.login_error.time.sleep")
    @patch("features.login_error.open_anydesk")
    def test_login_error_uses_configurable_invalid_password(
        self,
        open_anydesk_mock,
        _sleep_mock,
        click_image_mock,
        click_coordinates_mock,
        _save_screenshot_mock,
        assert_image_visible_mock,
    ):
        login_error.run()

        open_anydesk_mock.assert_called_once_with()
        click_coordinates_mock.assert_called_once_with(660, 310)
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call("login_button.png"),
                call("login_two_button.png", timeout=10),
                call("login_one_button.png", timeout=10),
                call("login_two_button.png", timeout=10),
                call("login_three_button.png", timeout=10),
                call("login_four_button.png", timeout=10),
                call("login_five_button.png", timeout=10),
                call("login_one_button.png", timeout=10),
                call("entry_button.png"),
            ],
        )
        assert_image_visible_mock.assert_called_once_with(
            "login_error.png",
            confidence=0.80,
            timeout=15,
        )


if __name__ == "__main__":
    unittest.main()
