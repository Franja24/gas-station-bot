import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_suite = lambda cases: {"suite_cases": []}

cleanup_after_fueling_stub = types.ModuleType("features.cleanup_after_fueling")
cleanup_after_fueling_stub.run = lambda: None

cleanup_after_hose_unhooked_stub = types.ModuleType(
    "features.cleanup_after_hose_unhooked"
)
cleanup_after_hose_unhooked_stub.run = lambda: None

close_at_payment_stub = types.ModuleType("features.close_at_payment_screen_e2e")
close_at_payment_stub.run = lambda: None

close_fueling_stub = types.ModuleType(
    "features.close_while_fueling_from_product_selection_e2e"
)
close_fueling_stub.run = lambda: None

close_unhooked_stub = types.ModuleType(
    "features.close_with_hose_unhooked_from_product_selection_e2e"
)
close_unhooked_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.cleanup_after_fueling": cleanup_after_fueling_stub,
    "features.cleanup_after_hose_unhooked": cleanup_after_hose_unhooked_stub,
    "features.close_at_payment_screen_e2e": close_at_payment_stub,
    "features.close_while_fueling_from_product_selection_e2e": close_fueling_stub,
    "features.close_with_hose_unhooked_from_product_selection_e2e": close_unhooked_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
close_kiosk_suite = importlib.import_module("features.close_kiosk_suite")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "cleanup_after_fueling",
        "cleanup_after_hose_unhooked",
        "close_at_payment_screen_e2e",
        "close_while_fueling_from_product_selection_e2e",
        "close_with_hose_unhooked_from_product_selection_e2e",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class CloseKioskSuiteTests(unittest.TestCase):
    @patch("features.close_kiosk_suite.run_suite")
    def test_runs_close_kiosk_cases_in_requested_order(self, run_suite_mock):
        expected_result = {"suite_cases": []}
        run_suite_mock.return_value = expected_result

        result = close_kiosk_suite.run()

        self.assertIs(result, expected_result)
        cases = run_suite_mock.call_args.args[0]
        self.assertEqual(
            [case[0] for case in cases],
            [
                "02_close_with_hose_unhooked",
                "02_5_cleanup_after_hose_unhooked",
            ],
        )
        self.assertEqual(
            [case[1] for case in cases],
            [
                close_kiosk_suite.close_with_hose_unhooked_e2e_run,
                close_kiosk_suite.cleanup_after_hose_unhooked_run,
            ],
        )
        self.assertEqual(
            [
                case[2].get("reportable", True) if len(case) > 2 else True
                for case in cases
            ],
            [True, False],
        )


if __name__ == "__main__":
    unittest.main()
