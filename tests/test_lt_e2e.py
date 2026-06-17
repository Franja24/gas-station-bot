import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_stages = lambda stages: {"stages": []}

open_kiosco_stub = types.ModuleType("features.open_kiosco")
open_kiosco_stub.run = lambda: None

login_stub = types.ModuleType("features.login")
login_stub.run = lambda: None

change_type_charge_stub = types.ModuleType("features.change_type_charge")
change_type_charge_stub.run = lambda: None

windows_stub = types.ModuleType("features.windows_app")
windows_stub.run = lambda: None

invoice_stub = types.ModuleType("features.invoice")
invoice_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.open_kiosco": open_kiosco_stub,
    "features.login": login_stub,
    "features.change_type_charge": change_type_charge_stub,
    "features.windows_app": windows_stub,
    "features.invoice": invoice_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
lt_e2e = importlib.import_module("features.lt_e2e")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "open_kiosco",
        "login",
        "change_type_charge",
        "windows_app",
        "invoice",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class LtE2EFlowTests(unittest.TestCase):
    @patch("features.lt_e2e.run_stages")
    def test_runs_liters_e2e_flow_as_reportable_stages(self, run_stages_mock):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = lt_e2e.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "03_change_type_charge",
                "04_windows",
                "05_invoice",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                lt_e2e.change_type_charge_run,
                lt_e2e.windows_run,
                lt_e2e.invoice_run,
            ],
        )


if __name__ == "__main__":
    unittest.main()
