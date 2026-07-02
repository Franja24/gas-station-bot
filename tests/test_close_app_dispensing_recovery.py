import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_stages = lambda stages: {"stages": []}

magna_stub = types.ModuleType("features.magna")
magna_stub.run = lambda: None

windows_close_stub = types.ModuleType("features.windows_app_close_app")
windows_close_stub.run = lambda: None

open_kiosco_stub = types.ModuleType("features.open_kiosco")
open_kiosco_stub.run = lambda: None

sale_recovery_stub = types.ModuleType("features.sale_confirmation_recovery")
sale_recovery_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.magna": magna_stub,
    "features.windows_app_close_app": windows_close_stub,
    "features.open_kiosco": open_kiosco_stub,
    "features.sale_confirmation_recovery": sale_recovery_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
close_app_dispensing_recovery = importlib.import_module(
    "features.close_app_dispensing_recovery"
)

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "magna",
        "windows_app_close_app",
        "open_kiosco",
        "sale_confirmation_recovery",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class CloseAppDispensingRecoveryFlowTests(unittest.TestCase):
    @patch("features.close_app_dispensing_recovery.run_stages")
    def test_runs_from_start_screen_and_recovers_sale(self, run_stages_mock):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = close_app_dispensing_recovery.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "01_magna",
                "02_close_app_while_dispensing",
                "03_open_kiosco",
                "04_sale_confirmation_recovery",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                close_app_dispensing_recovery.magna_run,
                close_app_dispensing_recovery.windows_app_close_run,
                close_app_dispensing_recovery.open_kiosco_run,
                close_app_dispensing_recovery.sale_confirmation_recovery_run,
            ],
        )


if __name__ == "__main__":
    unittest.main()
