import unittest
from types import SimpleNamespace
from unittest.mock import call, patch

from features import login, login_error


class LoginFlowTests(unittest.TestCase):
    @patch("features.login.enter_from_start_screen", return_value=True)
    @patch("features.login.is_product_selection_visible")
    @patch("features.login.find_login_form")
    def test_open_login_form_enters_from_start_screen(
        self,
        find_login_form_mock,
        is_product_selection_visible_mock,
        enter_from_start_screen_mock,
    ):
        find_login_form_mock.return_value = None
        is_product_selection_visible_mock.side_effect = [False, True]

        form = login.open_login_form()

        self.assertIsNone(form)
        enter_from_start_screen_mock.assert_called_once_with()

    @patch("features.login.save_screenshot")
    @patch("features.login.open_login_form", return_value=None)
    @patch("features.login.open_anydesk")
    def test_login_returns_when_session_is_already_active(
        self,
        open_anydesk_mock,
        open_login_form_mock,
        save_screenshot_mock,
    ):
        login.run()

        open_anydesk_mock.assert_called_once_with()
        open_login_form_mock.assert_called_once_with()
        save_screenshot_mock.assert_called_once_with("00_login_already_active")

    @patch("features.login.assert_image_visible")
    @patch("features.login.save_screenshot")
    @patch("features.login.click_coordinates")
    @patch("features.login.click_image")
    @patch("features.login.pyautogui.press")
    @patch("features.login.pyautogui.hotkey")
    @patch("features.login.time.sleep")
    @patch("features.login.is_product_selection_visible", return_value=False)
    @patch("features.login.find_login_form")
    @patch("features.login.open_anydesk")
    def test_login_uses_configurable_id_and_password(
        self,
        open_anydesk_mock,
        find_login_form_mock,
        _is_product_selection_visible_mock,
        _sleep_mock,
        hotkey_mock,
        press_mock,
        click_image_mock,
        click_coordinates_mock,
        _save_screenshot_mock,
        assert_image_visible_mock,
    ):
        find_login_form_mock.return_value = SimpleNamespace(x=1280, y=600)

        login.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(click_coordinates_mock.call_count, 9)
        self.assertEqual(
            hotkey_mock.call_args_list,
            [
                call("ctrl", "a"),
                call("ctrl", "a"),
            ],
        )
        self.assertEqual(
            press_mock.call_args_list,
            [
                call("backspace"),
                call("backspace"),
            ],
        )
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "entry_button.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                    region=None,
                ),
                call(
                    "activate_unit.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                    region=None,
                ),
                call(
                    "start.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                    region=None,
                ),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call("activate_unit.png", confidence=0.80, timeout=15),
                call("start.png", confidence=0.80, timeout=15),
                call("premium.png", confidence=0.80, timeout=15),
            ],
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
