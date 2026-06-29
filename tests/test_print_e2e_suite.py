import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_suite = lambda cases: {"suite_cases": []}

print_e2e_100_stub = types.ModuleType("features.print_e2e")
print_e2e_100_stub.run = lambda: None

print_e2e_150_stub = types.ModuleType("features.print_e2e_150")
print_e2e_150_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.print_e2e": print_e2e_100_stub,
    "features.print_e2e_150": print_e2e_150_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
print_e2e_suite = importlib.import_module("features.print_e2e_suite")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "print_e2e",
        "print_e2e_150",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class PrintE2ESuiteTests(unittest.TestCase):
    @patch("features.print_e2e_suite.run_suite")
    def test_runs_100_and_150_print_flows_as_suite(self, run_suite_mock):
        expected_result = {"suite_cases": []}
        run_suite_mock.return_value = expected_result

        result = print_e2e_suite.run()

        self.assertIs(result, expected_result)
        cases = run_suite_mock.call_args.args[0]
        self.assertEqual(
            [case_name for case_name, _case_function in cases],
            [
                "01_print_e2e_100",
                "02_print_e2e_150",
            ],
        )
        self.assertEqual(
            [case_function for _case_name, case_function in cases],
            [
                print_e2e_suite.print_e2e_100_run,
                print_e2e_suite.print_e2e_150_run,
            ],
        )


if __name__ == "__main__":
    unittest.main()
