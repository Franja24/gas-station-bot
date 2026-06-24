import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_suite = lambda cases: {"suite_cases": []}

cancel_e2e_stub = types.ModuleType("features.cancel_e2e")
cancel_e2e_stub.run = lambda: None

close_app_e2e_stub = types.ModuleType("features.close_app_e2e")
close_app_e2e_stub.run = lambda: None

e2e_stub = types.ModuleType("features.e2e")
e2e_stub.run = lambda: None

lt_e2e_stub = types.ModuleType("features.lt_e2e")
lt_e2e_stub.run = lambda: None

sevenly_e2e_stub = types.ModuleType("features.sevenly_e2e")
sevenly_e2e_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.cancel_e2e": cancel_e2e_stub,
    "features.close_app_e2e": close_app_e2e_stub,
    "features.e2e": e2e_stub,
    "features.lt_e2e": lt_e2e_stub,
    "features.sevenly_e2e": sevenly_e2e_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
e2e_set_5 = importlib.import_module("features.e2e_set_5")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "cancel_e2e",
        "close_app_e2e",
        "e2e",
        "lt_e2e",
        "sevenly_e2e",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class E2ESet5Tests(unittest.TestCase):
    @patch("features.e2e_set_5.run_suite")
    def test_runs_five_e2e_cases_as_suite(self, run_suite_mock):
        expected_result = {"suite_cases": []}
        run_suite_mock.return_value = expected_result

        result = e2e_set_5.run()

        self.assertIs(result, expected_result)
        cases = run_suite_mock.call_args.args[0]
        self.assertEqual(
            [case_name for case_name, _case_function in cases],
            [
                "01_e2e",
                "02_sevenly_e2e",
                "03_cancel_e2e",
                "04_lt_e2e",
                "05_close_app_e2e",
            ],
        )
        self.assertEqual(
            [case_function for _case_name, case_function in cases],
            [
                e2e_set_5.e2e_run,
                e2e_set_5.sevenly_e2e_run,
                e2e_set_5.cancel_e2e_run,
                e2e_set_5.lt_e2e_run,
                e2e_set_5.close_app_e2e_run,
            ],
        )


if __name__ == "__main__":
    unittest.main()
