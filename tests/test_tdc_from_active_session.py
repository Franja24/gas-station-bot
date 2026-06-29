import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_stages = lambda stages: {"stages": []}

detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: None

active_session_start_stub = types.ModuleType("features.active_session_start")
active_session_start_stub.run = lambda: None

magna_amount_200_stub = types.ModuleType("features.magna_amount_200")
magna_amount_200_stub.run = lambda: None

open_kiosco_stub = types.ModuleType("features.open_kiosco")
open_kiosco_stub.run = lambda: None

windows_stub = types.ModuleType("features.windows_app")
windows_stub.run = lambda: None

print_ticket_stub = types.ModuleType("features.print_ticket")
print_ticket_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "detector": detector_stub,
    "features.active_session_start": active_session_start_stub,
    "features.magna_amount_200": magna_amount_200_stub,
    "features.open_kiosco": open_kiosco_stub,
    "features.windows_app": windows_stub,
    "features.print_ticket": print_ticket_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
tdc_from_active_session = importlib.import_module(
    "features.tdc_from_active_session"
)

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "active_session_start",
        "magna_amount_200",
        "open_kiosco",
        "windows_app",
        "print_ticket",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class TDCFromActiveSessionFlowTests(unittest.TestCase):
    @patch("features.tdc_from_active_session.run_stages")
    def test_runs_tdc_from_active_session_without_login_stages(
        self,
        run_stages_mock,
    ):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result

        result = tdc_from_active_session.run()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "00_open_kiosco",
                "01_active_session_start",
                "02_magna_amount_200",
                "03_windows",
                "04_print_ticket",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                tdc_from_active_session.open_kiosco_run,
                tdc_from_active_session.active_session_start_run,
                tdc_from_active_session.magna_amount_200_run,
                tdc_from_active_session.windows_run,
                tdc_from_active_session.print_ticket_run,
            ],
        )

    @patch("features.tdc_from_active_session.run_stages")
    @patch("features.tdc_from_active_session.find_image")
    def test_runs_tdc_from_current_start_screen_without_open_kiosco(
        self,
        find_image_mock,
        run_stages_mock,
    ):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result
        find_image_mock.return_value = None

        result = tdc_from_active_session.run_from_start_screen()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "00_active_session_start",
                "01_magna_amount_200",
                "02_windows",
                "03_print_ticket",
            ],
        )
        self.assertEqual(
            [stage_function for _stage_name, stage_function in stages],
            [
                tdc_from_active_session.active_session_start_run,
                tdc_from_active_session.magna_amount_200_run,
                tdc_from_active_session.windows_run,
                tdc_from_active_session.print_ticket_run,
            ],
        )

    @patch("features.tdc_from_active_session.run_stages")
    @patch("features.tdc_from_active_session.find_image")
    def test_resumes_tdc_from_payment_success(
        self,
        find_image_mock,
        run_stages_mock,
    ):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result
        find_image_mock.return_value = object()

        result = tdc_from_active_session.run_from_start_screen()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "00_windows",
                "01_print_ticket",
            ],
        )

    @patch("features.tdc_from_active_session.run_stages")
    @patch("features.tdc_from_active_session.find_image")
    def test_resumes_tdc_from_product_selection(
        self,
        find_image_mock,
        run_stages_mock,
    ):
        expected_result = {"stages": []}
        run_stages_mock.return_value = expected_result
        find_image_mock.side_effect = [None, object(), object()]

        result = tdc_from_active_session.run_from_start_screen()

        self.assertIs(result, expected_result)
        stages = run_stages_mock.call_args.args[0]
        self.assertEqual(
            [stage_name for stage_name, _stage_function in stages],
            [
                "00_magna_amount_200",
                "01_windows",
                "02_print_ticket",
            ],
        )


if __name__ == "__main__":
    unittest.main()
