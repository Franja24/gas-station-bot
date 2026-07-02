import importlib
import sys
import types
import unittest
from unittest.mock import patch


applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("screenshot", screenshot_stub)

print_feature = importlib.import_module("features.print")


class PrintFlowTests(unittest.TestCase):
    @patch("features.print.open_anydesk")
    @patch("features.print.time.sleep")
    @patch("features.print.save_screenshot")
    @patch("features.print.assert_image_visible")
    @patch("features.print.click_image")
    def test_prints_ticket_and_finishes_with_calibrated_continue(
        self,
        click_image_mock,
        assert_image_visible_mock,
        save_screenshot_mock,
        sleep_mock,
        open_anydesk_mock,
    ):
        print_feature.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                unittest.mock.call(
                    "print.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                unittest.mock.call(
                    "print_continue_button.png",
                    timeout=10,
                    use_coordinates=True,
                    use_region=False,
                ),
            ],
        )
        assert_image_visible_mock.assert_called_once_with(
            "magna.png",
            confidence=0.80,
            timeout=15,
        )
        self.assertEqual(
            save_screenshot_mock.call_args_list,
            [
                unittest.mock.call("step_1_print_clicked"),
                unittest.mock.call("step_2_finish_flow"),
            ],
        )
        self.assertEqual(
            sleep_mock.call_args_list,
            [
                unittest.mock.call(2),
                unittest.mock.call(2),
            ],
        )


if __name__ == "__main__":
    unittest.main()
