import unittest
from unittest.mock import call, patch

from features import change_employee_assisted


class ChangeEmployeeAssistedTests(unittest.TestCase):
    @patch("features.change_employee_assisted.save_screenshot")
    @patch("features.change_employee_assisted.assert_image_visible")
    def test_waits_for_human_card_and_captures_employee_screen(
        self,
        assert_visible_mock,
        save_screenshot_mock,
    ):
        change_employee_assisted._wait_for_employee_card("6")

        assert_visible_mock.assert_called_once_with(
            "change_employee_activate_button.png",
            confidence=0.80,
            timeout=change_employee_assisted.HUMAN_CARD_TIMEOUT_SECONDS,
        )
        save_screenshot_mock.assert_called_once_with(
            "employee_6_change_screen"
        )

    @patch("features.change_employee_assisted.save_screenshot")
    @patch("features.change_employee_assisted.assert_image_visible")
    @patch("features.change_employee_assisted.click_asset")
    def test_activates_employee_and_waits_for_welcome(
        self,
        click_asset_mock,
        assert_visible_mock,
        save_screenshot_mock,
    ):
        change_employee_assisted._activate_employee("7")

        click_asset_mock.assert_called_once_with(
            "change_employee_activate_button.png",
            timeout=10,
        )
        assert_visible_mock.assert_called_once_with(
            "activate_unit_button.png",
            confidence=0.80,
            timeout=15,
        )
        save_screenshot_mock.assert_called_once_with(
            "employee_7_welcome_screen"
        )

    @patch("features.change_employee_assisted.save_screenshot")
    @patch("features.change_employee_assisted.assert_image_visible")
    @patch("features.change_employee_assisted.click_asset")
    def test_activates_unit_and_leaves_start_ready_for_next_card(
        self,
        click_asset_mock,
        assert_visible_mock,
        save_screenshot_mock,
    ):
        change_employee_assisted._activate_unit("5")

        click_asset_mock.assert_called_once_with(
            "activate_unit_button.png",
            timeout=10,
        )
        assert_visible_mock.assert_called_once_with(
            "start.png",
            confidence=0.80,
            timeout=15,
        )
        save_screenshot_mock.assert_called_once_with(
            "employee_5_start_ready"
        )

    @patch("features.change_employee_assisted.run_stages")
    def test_runs_four_employee_changes_in_one_case(self, run_stages_mock):
        run_stages_mock.return_value = {"stages": []}

        change_employee_assisted.run(iterations=4)

        stages = run_stages_mock.call_args.args[0]
        stage_names = [name for name, _function in stages]
        self.assertEqual(len(stage_names), 13)
        self.assertEqual(
            stage_names,
            [
                "00_focus_product_selection",
                "01_wait_card_employee_7",
                "01_activate_employee_7",
                "01_activate_unit_employee_7",
                "02_wait_card_employee_6",
                "02_activate_employee_6",
                "02_activate_unit_employee_6",
                "03_wait_card_employee_5",
                "03_activate_employee_5",
                "03_activate_unit_employee_5",
                "04_wait_card_employee_8",
                "04_activate_employee_8",
                "04_activate_unit_employee_8",
            ],
        )

        with (
            patch.object(change_employee_assisted, "_wait_for_employee_card") as wait_mock,
            patch.object(change_employee_assisted, "_activate_employee") as activate_mock,
            patch.object(change_employee_assisted, "_activate_unit") as unit_mock,
        ):
            for _name, function in stages[1:]:
                function()

        self.assertEqual(
            wait_mock.call_args_list,
            [call("7"), call("6"), call("5"), call("8")],
        )
        self.assertEqual(
            activate_mock.call_args_list,
            [call("7"), call("6"), call("5"), call("8")],
        )
        self.assertEqual(
            unit_mock.call_args_list,
            [call("7"), call("6"), call("5"), call("8")],
        )


if __name__ == "__main__":
    unittest.main()
