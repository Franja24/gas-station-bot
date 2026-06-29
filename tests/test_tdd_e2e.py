import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_stages = lambda stages: {"stages": []}

login_stub = types.ModuleType("features.login")
login_stub.run = lambda: None

sevenly_login_stub = types.ModuleType("features.sevenly_login")
sevenly_login_stub.run = lambda: None

magna_amount_100_stub = types.ModuleType("features.magna_amount_100")
magna_amount_100_stub.run = lambda: None

open_kiosco_stub = types.ModuleType("features.open_kiosco")
open_kiosco_stub.run = lambda: None

windows_stub = types.ModuleType("features.windows_app")
windows_stub.run = lambda: None

print_ticket_stub = types.ModuleType("features.print_ticket")
print_ticket_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.login": login_stub,
    "features.sevenly_login": sevenly_login_stub,
    "features.magna_amount_100": magna_amount_100_stub,
    "features.open_kiosco": open_kiosco_stub,
    "features.windows_app": windows_stub,
    "features.print_ticket": print_ticket_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
tdd_e2e = importlib.import_module("features.tdd_e2e")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "login",
        "sevenly_login",
        "magna_amount_100",
        "open_kiosco",
        "windows_app",
        "print_ticket",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class TDDE2EFlowTests(unittest.TestCase):
    @patch("features.tdd_e2e.run_stages")
    def test_runs_tdd_amount_100_e2e_as_reportable_stages(self, run_stages_mock):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = tdd_e2e.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "00_open_kiosco",
                "01_login",
                "02_sevenly_login",
                "03_magna_amount_100",
                "04_windows",
                "05_print_ticket",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                tdd_e2e.open_kiosco_run,
                tdd_e2e.login_run,
                tdd_e2e.sevenly_login_run,
                tdd_e2e.magna_amount_100_run,
                tdd_e2e.windows_run,
                tdd_e2e.print_ticket_run,
            ],
        )


if __name__ == "__main__":
    unittest.main()
