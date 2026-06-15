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

magna_stub = types.ModuleType("features.magna")
magna_stub.run = lambda: None

windows_close_stub = types.ModuleType("features.windows_app_close_app")
windows_close_stub.run = lambda: None

open_kiosco_stub = types.ModuleType("features.open_kiosco")
open_kiosco_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.login": login_stub,
    "features.sevenly_login": sevenly_login_stub,
    "features.magna": magna_stub,
    "features.windows_app_close_app": windows_close_stub,
    "features.open_kiosco": open_kiosco_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
close_bump_e2e = importlib.import_module("features.close_bump_e2e")

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
        "magna",
        "windows_app_close_app",
        "open_kiosco",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class CloseBumpE2EFlowTests(unittest.TestCase):
    @patch("features.close_bump_e2e.run_stages")
    def test_runs_login_magna_windows_and_reopens_kiosco(self, run_stages_mock):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = close_bump_e2e.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "01_login",
                "02_sevenly_login",
                "03_magna",
                "04_windows",
                "05_open_kiosco",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                close_bump_e2e.login_run,
                close_bump_e2e.sevenly_login_run,
                close_bump_e2e.magna_run,
                close_bump_e2e.windows_close_run,
                close_bump_e2e.open_kiosco_run,
            ],
        )


if __name__ == "__main__":
    unittest.main()
