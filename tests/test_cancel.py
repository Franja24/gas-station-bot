import unittest
import sys
import types
from unittest.mock import patch

clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("screenshot", screenshot_stub)

from features import cancel


class CancelFlowTests(unittest.TestCase):
    @patch("features.cancel.assert_image_visible")
    @patch("features.cancel.save_screenshot")
    @patch("features.cancel.click_image")
    @patch("features.cancel.time.sleep")
    def test_cancels_service_and_returns_to_start(
        self,
        sleep_mock,
        click_image_mock,
        save_screenshot_mock,
        assert_image_visible_mock,
    ):
        cancel.run()

        self.assertEqual(
            click_image_mock.call_args_list,
            [
                unittest.mock.call(
                    "cancel_service_button.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                unittest.mock.call(
                    "finalize_button.png",
                    timeout=10,
                    use_coordinates=True,
                    use_region=False,
                ),
            ],
        )
        self.assertEqual(
            assert_image_visible_mock.call_args_list,
            [
                unittest.mock.call(
                    "purchase_summary_title.png",
                    confidence=0.80,
                    timeout=15,
                ),
                unittest.mock.call(
                    "iniciar.png",
                    confidence=0.85,
                    timeout=15,
                ),
            ],
        )
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                unittest.mock.call("step_1_cancel_service_clicked"),
                unittest.mock.call("step_2_purchase_summary_visible"),
                unittest.mock.call("step_3_finalize_clicked"),
                unittest.mock.call("step_4_start_screen_visible"),
            ],
        )
        sleep_mock.assert_called_once_with(2)


if __name__ == "__main__":
    unittest.main()
