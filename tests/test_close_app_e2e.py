import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_stages = lambda stages: {"stages": []}

confirm_transaction_stub = types.ModuleType("features.confirm_transaction")
confirm_transaction_stub.run = lambda: None

login_for_confirm_stub = types.ModuleType("features.login_for_confirm_transaction")
login_for_confirm_stub.run = lambda: None

open_kiosco_ready_stub = types.ModuleType("features.open_kiosco_ready")
open_kiosco_ready_stub.run = lambda: None

login_if_needed_stub = types.ModuleType("features.login_if_needed")
login_if_needed_stub.run = lambda: None

magna_stub = types.ModuleType("features.magna")
magna_stub.run = lambda: None

windows_close_stub = types.ModuleType("features.windows_app_close_app")
windows_close_stub.run = lambda: None

windows_hang_up_stub = types.ModuleType("features.windows_app_hang_up")
windows_hang_up_stub.run = lambda: None

validate_product_selection_stub = types.ModuleType(
    "features.validate_product_selection"
)
validate_product_selection_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.confirm_transaction": confirm_transaction_stub,
    "features.login_for_confirm_transaction": login_for_confirm_stub,
    "features.open_kiosco_ready": open_kiosco_ready_stub,
    "features.login_if_needed": login_if_needed_stub,
    "features.magna": magna_stub,
    "features.windows_app_close_app": windows_close_stub,
    "features.windows_app_hang_up": windows_hang_up_stub,
    "features.validate_product_selection": validate_product_selection_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
close_app_e2e = importlib.import_module("features.close_app_e2e")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "confirm_transaction",
        "login_for_confirm_transaction",
        "open_kiosco_ready",
        "login_if_needed",
        "magna",
        "windows_app_close_app",
        "windows_app_hang_up",
        "validate_product_selection",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class CloseAppE2EFlowTests(unittest.TestCase):
    @patch("features.close_app_e2e.run_stages")
    def test_opens_kiosco_runs_flow_and_reopens_kiosco(self, run_stages_mock):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = close_app_e2e.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "01_open_kiosco",
                "02_login_if_needed",
                "03_magna_to_instructions",
                "04_windows_app_close",
                "05_windows_app_hang_up",
                "06_open_kiosco",
                "07_login_for_confirm",
                "08_confirm_transaction",
                "09_validate_product_selection",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                close_app_e2e.open_kiosco_ready_run,
                close_app_e2e.login_if_needed_run,
                close_app_e2e.magna_run,
                close_app_e2e.windows_app_close_run,
                close_app_e2e.windows_app_hang_up_run,
                close_app_e2e.open_kiosco_ready_run,
                close_app_e2e.login_for_confirm_run,
                close_app_e2e.confirm_transaction_run,
                close_app_e2e.validate_product_selection_run,
            ],
        )


if __name__ == "__main__":
    unittest.main()
