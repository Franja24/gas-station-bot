import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_suite = lambda cases: {"suite_cases": []}

tdd_e2e_stub = types.ModuleType("features.tdd_e2e")
tdd_e2e_stub.run = lambda: None

tdc_from_active_session_stub = types.ModuleType(
    "features.tdc_from_active_session"
)
tdc_from_active_session_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.tdd_e2e": tdd_e2e_stub,
    "features.tdc_from_active_session": tdc_from_active_session_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
card_payments_suite = importlib.import_module("features.card_payments_suite")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "tdd_e2e",
        "tdc_from_active_session",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class CardPaymentsSuiteTests(unittest.TestCase):
    @patch("features.card_payments_suite.run_suite")
    def test_runs_tdd_and_tdc_cases_as_suite(self, run_suite_mock):
        expected_result = {"suite_cases": []}
        run_suite_mock.return_value = expected_result

        result = card_payments_suite.run()

        self.assertIs(result, expected_result)
        cases = run_suite_mock.call_args.args[0]
        self.assertEqual(
            [case_name for case_name, _case_function in cases],
            [
                "01_tdd_e2e",
                "02_tdc_from_active_session",
            ],
        )
        self.assertEqual(
            [case_function for _case_name, case_function in cases],
            [
                card_payments_suite.tdd_e2e_run,
                card_payments_suite.tdc_from_active_session_run,
            ],
        )


if __name__ == "__main__":
    unittest.main()
