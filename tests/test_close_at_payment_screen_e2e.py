import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_stages = lambda stages: {"stages": []}

kiosk_process_stub = types.ModuleType("features.kiosk_process")
kiosk_process_stub.run = lambda: None

login_if_needed_stub = types.ModuleType("features.login_if_needed")
login_if_needed_stub.run = lambda: None

magna_amount_100_stub = types.ModuleType("features.magna_amount_100")
magna_amount_100_stub.run = lambda: None

open_kiosco_ready_stub = types.ModuleType("features.open_kiosco_ready")
open_kiosco_ready_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.kiosk_process": kiosk_process_stub,
    "features.login_if_needed": login_if_needed_stub,
    "features.magna_amount_100": magna_amount_100_stub,
    "features.open_kiosco_ready": open_kiosco_ready_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
close_at_payment_screen_e2e = importlib.import_module(
    "features.close_at_payment_screen_e2e"
)

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module


class CloseAtPaymentScreenE2ETests(unittest.TestCase):
    @patch("features.close_at_payment_screen_e2e.run_stages")
    def test_runs_payment_screen_close_and_reopens_at_login_boundary(
        self,
        run_stages_mock,
    ):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = close_at_payment_screen_e2e.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "01_open_kiosco",
                "02_login_if_needed",
                "03_magna_amount_100_to_instructions",
                "04_close_kiosk_at_payment_screen",
                "05_open_kiosco",
            ],
        )


if __name__ == "__main__":
    unittest.main()
