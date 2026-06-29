import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_stages = lambda stages: {"stages": []}

active_session_start_stub = types.ModuleType("features.active_session_start")
active_session_start_stub.run = lambda: None

magna_amount_150_stub = types.ModuleType("features.magna_amount_150")
magna_amount_150_stub.run = lambda: None

windows_stub = types.ModuleType("features.windows_app")
windows_stub.run = lambda: None

print_ticket_stub = types.ModuleType("features.print_ticket")
print_ticket_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.active_session_start": active_session_start_stub,
    "features.magna_amount_150": magna_amount_150_stub,
    "features.windows_app": windows_stub,
    "features.print_ticket": print_ticket_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
print_e2e_150 = importlib.import_module("features.print_e2e_150")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "active_session_start",
        "magna_amount_150",
        "windows_app",
        "print_ticket",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class PrintE2E150FlowTests(unittest.TestCase):
    @patch("features.print_e2e_150.run_stages")
    def test_runs_print_e2e_150_from_active_start_to_ticket(
        self,
        run_stages_mock,
    ):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = print_e2e_150.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "00_active_session_start",
                "01_magna_amount_150",
                "02_windows",
                "03_print_ticket",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                print_e2e_150.active_session_start_run,
                print_e2e_150.magna_amount_150_run,
                print_e2e_150.windows_run,
                print_e2e_150.print_ticket_run,
            ],
        )


if __name__ == "__main__":
    unittest.main()
