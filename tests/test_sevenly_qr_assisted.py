import unittest
from unittest.mock import call, patch

from features import sevenly_qr_assisted


class SevenlyQrAssistedTests(unittest.TestCase):
    @patch("features.sevenly_qr_assisted.save_screenshot")
    @patch("features.sevenly_qr_assisted.click_asset")
    @patch("features.sevenly_qr_assisted.assert_image_visible")
    @patch("features.sevenly_qr_assisted.click_sevenly_account")
    @patch("features.sevenly_qr_assisted.open_anydesk")
    def test_first_case_opens_sevenly_and_selects_qr(
        self,
        open_anydesk_mock,
        click_account_mock,
        assert_visible_mock,
        click_asset_mock,
        save_screenshot_mock,
    ):
        sevenly_qr_assisted._open_qr_scanner()

        open_anydesk_mock.assert_called_once_with()
        click_account_mock.assert_called_once_with()
        assert_visible_mock.assert_has_calls(
            [
                call("sevenly_qr_option.png", confidence=0.80, timeout=15),
                call("sevenly_qr_waiting.png", confidence=0.80, timeout=15),
            ]
        )
        click_asset_mock.assert_called_once_with(
            "sevenly_qr_option.png",
            timeout=10,
        )
        save_screenshot_mock.assert_called_once_with("sevenly_qr_ready")

    @patch("features.sevenly_qr_assisted.save_screenshot")
    @patch("features.sevenly_qr_assisted.click_asset")
    @patch("features.sevenly_qr_assisted._wait_until_previous_error_clears")
    @patch("features.sevenly_qr_assisted.assert_image_visible")
    @patch("features.sevenly_qr_assisted.open_anydesk")
    def test_second_case_reuses_screen_and_restarts_scanner(
        self,
        open_anydesk_mock,
        assert_visible_mock,
        clear_error_mock,
        click_asset_mock,
        save_screenshot_mock,
    ):
        sevenly_qr_assisted._restart_qr_scanner()

        open_anydesk_mock.assert_called_once_with()
        assert_visible_mock.assert_called_once_with(
            "sevenly_qr_waiting.png",
            confidence=0.80,
            timeout=15,
        )
        clear_error_mock.assert_called_once_with()
        click_asset_mock.assert_called_once_with(
            "sevenly_qr_scanner.png",
            timeout=10,
        )
        save_screenshot_mock.assert_called_once_with("sevenly_qr_restarted")

    @patch("features.sevenly_qr_assisted.save_screenshot")
    @patch("features.sevenly_qr_assisted.assert_image_visible")
    def test_error_finishes_assisted_case(
        self,
        assert_visible_mock,
        save_screenshot_mock,
    ):
        sevenly_qr_assisted._validate_error("Luis")

        assert_visible_mock.assert_called_once_with(
            "sevenly_error_toast.png",
            confidence=0.80,
            timeout=sevenly_qr_assisted.ERROR_TIMEOUT_SECONDS,
        )
        save_screenshot_mock.assert_called_once_with(
            "sevenly_qr_luis_error"
        )

    @patch("features.sevenly_qr_assisted.run_stages")
    def test_sachin_flow_uses_second_screen_sequence(self, run_stages_mock):
        run_stages_mock.return_value = {"stages": []}

        sevenly_qr_assisted.run("Sachin", first_case=False)

        stage_names = [name for name, _function in run_stages_mock.call_args.args[0]]
        self.assertEqual(
            stage_names,
            [
                "00_prepare_qr_sachin",
                "01_wait_human_qr_sachin",
                "02_validate_qr_error_sachin",
            ],
        )


if __name__ == "__main__":
    unittest.main()
