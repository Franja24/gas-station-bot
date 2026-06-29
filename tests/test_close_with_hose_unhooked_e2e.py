import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_stages = lambda stages: {"stages": []}

login_if_needed_stub = types.ModuleType("features.login_if_needed")
login_if_needed_stub.run = lambda: None

magna_stub = types.ModuleType("features.magna")
magna_stub.run = lambda: None

open_kiosco_ready_stub = types.ModuleType("features.open_kiosco_ready")
open_kiosco_ready_stub.run = lambda: None

validate_stub = types.ModuleType("features.validate_product_selection")
validate_stub.run = lambda: None

hang_up_stub = types.ModuleType("features.windows_app_hang_up")
hang_up_stub.run = lambda: None

unhook_close_stub = types.ModuleType("features.windows_app_unhook_close")
unhook_close_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.login_if_needed": login_if_needed_stub,
    "features.magna": magna_stub,
    "features.open_kiosco_ready": open_kiosco_ready_stub,
    "features.validate_product_selection": validate_stub,
    "features.windows_app_hang_up": hang_up_stub,
    "features.windows_app_unhook_close": unhook_close_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
close_with_hose_unhooked_e2e = importlib.import_module(
    "features.close_with_hose_unhooked_e2e"
)

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module


class CloseWithHoseUnhookedE2ETests(unittest.TestCase):
    @patch("features.close_with_hose_unhooked_e2e.run_stages")
    def test_runs_unhook_close_and_cleanup(self, run_stages_mock):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = close_with_hose_unhooked_e2e.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "01_open_kiosco",
                "02_login_if_needed",
                "03_magna_to_instructions",
                "04_windows_app_unhook_close",
                "05_windows_app_hang_up",
                "06_open_kiosco",
                "07_cleanup_out_of_service",
                "08_validate_product_selection",
            ],
        )


if __name__ == "__main__":
    unittest.main()
