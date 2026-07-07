from types import SimpleNamespace
import unittest
from unittest.mock import patch

from features.steps import flow_steps


class FlowStepsReportTests(unittest.TestCase):
    def test_table_flows_are_grouped_as_test_cases(self):
        context = SimpleNamespace(
            table=[
                {"flow": "normal_magna_1250"},
                {"flow": "normal_premium_500"},
            ],
            expected_flows=[],
            completed_flows=[],
            behave_stages=[
                {
                    "name": "open_kiosco",
                    "status": "PASSED",
                    "duration_seconds": 1.0,
                }
            ],
            behave_background_stages=[],
            behave_test_cases=[],
            behave_error=None,
        )

        def magna_flow():
            return {
                "stages": [
                    {
                        "name": "00_prepare_product_selection",
                        "status": "PASSED",
                        "duration_seconds": 1.0,
                    }
                ]
            }

        def premium_flow():
            return {
                "stages": [
                    {
                        "name": "02_select_product",
                        "status": "PASSED",
                        "duration_seconds": 2.0,
                    }
                ]
            }

        with (
            patch.dict(
                flow_steps.FLOW_RUNNERS,
                {
                    "normal_magna_1250": magna_flow,
                    "normal_premium_500": premium_flow,
                },
            ),
            patch.object(flow_steps.screenshot, "set_screenshot_case") as case_mock,
        ):
            flow_steps.step_run_flows(context)

        self.assertEqual(
            context.completed_flows,
            ["normal_magna_1250", "normal_premium_500"],
        )
        self.assertEqual(
            context.behave_background_stages[0]["name"],
            "open_kiosco",
        )
        self.assertEqual([case["id"] for case in context.behave_test_cases], [
            "TC01",
            "TC02",
        ])
        self.assertEqual(context.behave_test_cases[0]["name"], "normal_magna_1250")
        self.assertEqual(
            context.behave_test_cases[0]["stages"][0]["name"],
            "00_prepare_product_selection",
        )
        case_mock.assert_any_call("TC01_normal_magna_1250")
        case_mock.assert_any_call("TC02_normal_premium_500")
        self.assertEqual(case_mock.call_args_list[-1].args, (None,))

    def test_table_flows_can_use_matrix_case_ids(self):
        context = SimpleNamespace(
            table=[
                {
                    "case_id": "CP_AV_001",
                    "flow": "login",
                    "checkpoint": "Inicio de sesión estándar",
                }
            ],
            expected_flows=[],
            completed_flows=[],
            behave_stages=[],
            behave_background_stages=[],
            behave_test_cases=[],
            behave_error=None,
        )

        with (
            patch.dict(
                flow_steps.FLOW_RUNNERS,
                {
                    "login": lambda: {
                        "stages": [
                            {
                                "name": "01_login_start",
                                "status": "PASSED",
                                "duration_seconds": 1.0,
                            }
                        ]
                    },
                },
            ),
            patch.object(flow_steps.screenshot, "set_screenshot_case") as case_mock,
        ):
            flow_steps.step_run_flows(context)

        self.assertEqual(context.behave_test_cases[0]["id"], "CP_AV_001")
        self.assertEqual(
            context.behave_test_cases[0]["name"],
            "Inicio de sesión estándar",
        )
        self.assertEqual(context.behave_test_cases[0]["flow"], "login")
        case_mock.assert_any_call("CP_AV_001_login")

    def test_assisted_checkpoints_are_documented_without_running_a_flow(self):
        context = SimpleNamespace(
            table=[
                {
                    "case_id": "CP_AV_004",
                    "checkpoint": "Inicio RFID",
                    "bot_scope": "Evidencia visual",
                    "human_scope": "Lectura RFID física",
                }
            ],
            behave_test_cases=[],
        )

        flow_steps.step_register_assisted_checkpoints(context)
        flow_steps.step_assisted_checkpoints_documented(context)

        self.assertEqual(context.expected_assisted_checkpoints, ["CP_AV_004"])
        self.assertEqual(context.behave_test_cases[0]["status"], "ASSISTED")
        self.assertEqual(context.behave_test_cases[0]["flow"], "bot_humano")
        self.assertEqual(
            context.behave_test_cases[0]["stages"][1]["status"],
            "PENDING_HUMAN",
        )


if __name__ == "__main__":
    unittest.main()
