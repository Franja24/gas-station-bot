import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_stages = lambda stages: {"stages": []}

login_if_needed_stub = types.ModuleType("features.login_if_needed")
login_if_needed_stub.run = lambda: None

activate_unit_stub = types.ModuleType("features.activate_unit_for_out_of_service")
activate_unit_stub.run = lambda: None

magna_amount_150_stub = types.ModuleType("features.magna_amount_150_approved")
magna_amount_150_stub.run = lambda: None
magna_amount_150_stub.get_last_payment_result = lambda: "approved"

open_kiosco_ready_stub = types.ModuleType("features.open_kiosco_ready")
open_kiosco_ready_stub.run = lambda: None

validate_out_of_service_stub = types.ModuleType("features.validate_out_of_service")
validate_out_of_service_stub.run = lambda: None

unhook_close_stub = types.ModuleType("features.windows_app_unhook_close")
unhook_close_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.activate_unit_for_out_of_service": activate_unit_stub,
    "features.login_if_needed": login_if_needed_stub,
    "features.magna_amount_150_approved": magna_amount_150_stub,
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
    def test_starts_from_login_then_runs_magna_amount_150(
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
                "01_login_if_needed",
                "02_magna_amount_150_wait_for_payment_approval",
                "03_windows_app_unhook_close",
                "04_open_kiosco",
                "05_activate_unit_for_out_of_service",
                "06_validate_out_of_service",
            ],
        )
        self.assertIs(stages[0][1], flow.login_if_needed_run)
        self.assertIs(stages[1][1], flow.magna_amount_150_approved_run)
        self.assertIs(stages[2][1], flow.unhook_close_if_approved)

    @patch.object(flow, "get_last_payment_result", return_value="declined")
    @patch.object(flow, "windows_app_unhook_close_run")
    def test_skips_unhook_when_payment_is_declined(
        self,
        unhook_mock,
        _payment_result_mock,
    ):
        flow.unhook_close_if_approved()

        unhook_mock.assert_not_called()

    @patch.object(flow, "get_last_payment_result", return_value="approved")
    @patch.object(flow, "windows_app_unhook_close_run")
    def test_unhooks_when_payment_is_approved(
        self,
        unhook_mock,
        _payment_result_mock,
    ):
        flow.unhook_close_if_approved()

        unhook_mock.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
