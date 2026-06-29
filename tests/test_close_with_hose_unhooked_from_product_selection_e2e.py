import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_stages = lambda stages: {"stages": []}

magna_amount_100_stub = types.ModuleType("features.magna_amount_100")
magna_amount_100_stub.run = lambda: None

open_kiosco_ready_stub = types.ModuleType("features.open_kiosco_ready")
open_kiosco_ready_stub.run = lambda: None

validate_out_of_service_stub = types.ModuleType("features.validate_out_of_service")
validate_out_of_service_stub.run = lambda: None

unhook_close_stub = types.ModuleType("features.windows_app_unhook_close")
unhook_close_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.magna_amount_100": magna_amount_100_stub,
    "features.open_kiosco_ready": open_kiosco_ready_stub,
    "features.validate_out_of_service": validate_out_of_service_stub,
    "features.windows_app_unhook_close": unhook_close_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
flow = importlib.import_module(
    "features.close_with_hose_unhooked_from_product_selection_e2e"
)

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module


class CloseWithHoseUnhookedFromProductSelectionTests(unittest.TestCase):
    @patch(
        "features.close_with_hose_unhooked_from_product_selection_e2e.run_stages"
    )
    def test_starts_from_product_selection_with_magna_amount_100(
        self,
        run_stages_mock,
    ):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = flow.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "01_magna_amount_100_to_instructions",
                "02_windows_app_unhook_close",
                "03_open_kiosco",
                "04_validate_out_of_service",
            ],
        )
        self.assertIs(stages[0][1], flow.magna_amount_100_run)


if __name__ == "__main__":
    unittest.main()
