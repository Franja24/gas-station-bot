import importlib
import sys
import types
import unittest
from unittest.mock import patch


case_runner_stub = types.ModuleType("case_runner")
case_runner_stub.run_suite = lambda cases: {"suite_cases": []}

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

close_app_e2e_stub = types.ModuleType("features.close_app_e2e")
close_app_e2e_stub.run = lambda: None

close_bump_e2e_stub = types.ModuleType("features.close_bump_e2e")
close_bump_e2e_stub.run = lambda: None

manual_cancel_stub = types.ModuleType(
    "features.manual_cancel_last_transation"
)
manual_cancel_stub.run = lambda: None

open_kiosco_ready_stub = types.ModuleType("features.open_kiosco_ready")
open_kiosco_ready_stub.run = lambda: None

out_of_service_stub = types.ModuleType("features.out_of_service")
out_of_service_stub.is_out_of_service_visible = lambda *args, **kwargs: False

payment_screen_close_app_stub = types.ModuleType(
    "features.payment_screen_close_app"
)
payment_screen_close_app_stub.force_close_kiosk_process = lambda: None

payment_screen_close_e2e_stub = types.ModuleType(
    "features.payment_screen_close_e2e"
)
payment_screen_close_e2e_stub.run = lambda: None

_STUBBED_MODULES = {
    "case_runner": case_runner_stub,
    "features.applications": applications_stub,
    "features.close_app_e2e": close_app_e2e_stub,
    "features.close_bump_e2e": close_bump_e2e_stub,
    "features.manual_cancel_last_transation": manual_cancel_stub,
    "features.open_kiosco_ready": open_kiosco_ready_stub,
    "features.out_of_service": out_of_service_stub,
    "features.payment_screen_close_app": payment_screen_close_app_stub,
    "features.payment_screen_close_e2e": payment_screen_close_e2e_stub,
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
        "close_app_e2e",
        "close_bump_e2e",
        "applications",
        "manual_cancel_last_transation",
        "open_kiosco_ready",
        "out_of_service",
        "payment_screen_close_app",
        "payment_screen_close_e2e",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class CloseKioskSuiteTests(unittest.TestCase):
    @patch("features.close_kiosk_suite.run_suite")
    def test_runs_existing_close_kiosk_cases_as_suite(self, run_suite_mock):
        expected_result = {"suite_cases": []}
        run_suite_mock.return_value = expected_result

        result = close_kiosk_suite.run()

        self.assertIs(result, expected_result)
        cases = run_suite_mock.call_args.args[0]
        self.assertEqual(
            [case_name for case_name, _case_function in cases],
            [
                "01_close_at_payment_screen",
                "02_close_with_hose_hung_up",
                "03_close_while_fueling",
            ],
        )
        self.assertEqual(
            [case_function for _case_name, case_function in cases],
            [
                close_kiosk_suite.run_payment_screen_close_case,
                close_kiosk_suite.run_hose_hung_up_case,
                close_kiosk_suite.run_fueling_case,
            ],
        )

    @patch(
        "features.close_kiosk_suite.is_out_of_service_visible",
        return_value=False,
    )
    @patch("features.close_kiosk_suite.open_anydesk")
    def test_prepare_close_case_does_nothing_without_out_of_service_screen(
        self,
        open_anydesk_mock,
        is_out_of_service_visible_mock,
    ):
        close_kiosk_suite.prepare_close_case()

        open_anydesk_mock.assert_called_once_with()
        is_out_of_service_visible_mock.assert_called_once_with(timeout=3)

    @patch("features.close_kiosk_suite.force_close_kiosk_process")
    @patch("features.close_kiosk_suite.manual_cancel_last_transation_run")
    @patch(
        "features.close_kiosk_suite.is_out_of_service_visible",
        return_value=True,
    )
    @patch("features.close_kiosk_suite.open_anydesk")
    def test_prepare_close_case_recovers_out_of_service_screen(
        self,
        _open_anydesk_mock,
        _is_out_of_service_visible_mock,
        manual_cancel_last_transation_run_mock,
        force_close_kiosk_process_mock,
    ):
        close_kiosk_suite.prepare_close_case()

        manual_cancel_last_transation_run_mock.assert_called_once_with()
        force_close_kiosk_process_mock.assert_called_once_with()

    @patch("features.close_kiosk_suite.payment_screen_close_e2e_run")
    @patch("features.close_kiosk_suite.open_kiosco_ready_run")
    @patch("features.close_kiosk_suite.prepare_close_case")
    def test_payment_screen_case_opens_kiosk_first(
        self,
        prepare_close_case_mock,
        open_kiosco_ready_run_mock,
        payment_screen_close_e2e_run_mock,
    ):
        expected_result = {"stages": []}
        payment_screen_close_e2e_run_mock.return_value = expected_result

        result = close_kiosk_suite.run_payment_screen_close_case()

        self.assertIs(result, expected_result)
        prepare_close_case_mock.assert_called_once_with()
        open_kiosco_ready_run_mock.assert_called_once_with()
        payment_screen_close_e2e_run_mock.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
