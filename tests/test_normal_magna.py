import unittest
from types import SimpleNamespace
from unittest.mock import patch

from features import normal_magna


class NormalMagnaFlowTests(unittest.TestCase):
    @patch("features.normal_magna.run_stages")
    def test_runs_normal_magna_flow_as_reportable_stages(self, run_stages_mock):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = normal_magna.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "00_prepare_product_selection",
                "01_magna",
                "02_windows_app",
                "03_finalize_purchase_summary",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                normal_magna.prepare_product_selection,
                normal_magna.magna_run,
                normal_magna.windows_run,
                normal_magna.finalize_purchase_summary,
            ],
        )

    @patch("features.normal_magna.save_screenshot")
    @patch("features.normal_magna.time.sleep")
    @patch("features.normal_magna.click_coordinates")
    @patch("features.normal_magna.find_image")
    @patch("features.normal_magna.product_selection_visible")
    def test_click_start_button_uses_detected_button_position(
        self,
        product_selection_visible_mock,
        find_image_mock,
        click_coordinates_mock,
        _sleep_mock,
        save_screenshot_mock,
    ):
        product_selection_visible_mock.side_effect = [False, True]
        find_image_mock.return_value = SimpleNamespace(x=1197, y=735)

        normal_magna.click_start_button()

        click_coordinates_mock.assert_called_once_with(598, 367)
        save_screenshot_mock.assert_called_once_with("normal_magna_start_clicked")

    @patch("features.normal_magna.wait_for_start_or_product_selection")
    @patch("features.normal_magna.find_image")
    @patch("features.normal_magna.is_visible")
    @patch("features.normal_magna.time.sleep")
    @patch("features.normal_magna.click_image")
    @patch("features.normal_magna.assert_image_visible")
    def test_finalize_visible_purchase_summary_clicks_finalize_asset(
        self,
        assert_image_visible_mock,
        click_image_mock,
        _sleep_mock,
        is_visible_mock,
        find_image_mock,
        wait_for_start_or_product_selection_mock,
    ):
        is_visible_mock.return_value = False
        find_image_mock.return_value = None

        normal_magna.finalize_visible_purchase_summary()

        assert_image_visible_mock.assert_called_once_with(
            "purchase_summary_title.png",
            confidence=0.80,
            timeout=30,
        )
        click_image_mock.assert_called_once_with(
            "finalize_button.png",
            timeout=5,
            use_coordinates=False,
            use_region=False,
            region=normal_magna.FINALIZE_BUTTON_REGION,
        )
        wait_for_start_or_product_selection_mock.assert_called_once_with(timeout=30)


if __name__ == "__main__":
    unittest.main()
