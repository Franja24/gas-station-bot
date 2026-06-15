import unittest
import sys
import types
from unittest.mock import call, patch

clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

pyautogui_stub = types.ModuleType("pyautogui")
pyautogui_stub.hotkey = lambda *args, **kwargs: None

sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("screenshot", screenshot_stub)
sys.modules.setdefault("pyautogui", pyautogui_stub)

from features import premium_close_app


class PremiumCloseAppFlowTests(unittest.TestCase):
    @patch("features.premium_close_app.save_screenshot")
    @patch("features.premium_close_app.assert_image_visible")
    @patch("features.premium_close_app.click_image")
    @patch("features.premium_close_app.pyautogui.hotkey")
    @patch("features.premium_close_app.time.sleep")
    @patch("features.premium_close_app.open_anydesk")
    def test_selects_premium_amount_and_closes_with_alt_f4(
        self,
        open_anydesk_mock,
        _sleep_mock,
        hotkey_mock,
        click_image_mock,
        assert_image_visible_mock,
        save_screenshot_mock,
    ):
        premium_close_app.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "premium.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "amount_1250.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                call("amount_1250.png", confidence=0.80, timeout=10),
                call("continue_button.png", confidence=0.80, timeout=10),
            ],
        )
        hotkey_mock.assert_called_once_with("alt", "f4")
        save_screenshot_mock.assert_called_with(
            "step_3_alt_f4_close_attempt"
        )


if __name__ == "__main__":
    unittest.main()
