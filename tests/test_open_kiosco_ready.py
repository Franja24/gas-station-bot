import importlib
import sys
import types
import unittest
from unittest.mock import patch


applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

manual_cancel_stub = types.ModuleType(
    "features.manual_cancel_last_transation"
)
manual_cancel_stub.run = lambda: None

open_kiosco_stub = types.ModuleType("features.open_kiosco")
open_kiosco_stub.run = lambda: None

out_of_service_stub = types.ModuleType("features.out_of_service")
out_of_service_stub.is_out_of_service_visible = lambda *args, **kwargs: False

payment_screen_close_app_stub = types.ModuleType(
    "features.payment_screen_close_app"
)
payment_screen_close_app_stub.force_close_kiosk_process = lambda: None

_STUBBED_MODULES = {
    "features.applications": applications_stub,
    "features.manual_cancel_last_transation": manual_cancel_stub,
    "features.open_kiosco": open_kiosco_stub,
    "features.out_of_service": out_of_service_stub,
    "features.payment_screen_close_app": payment_screen_close_app_stub,
}

_original_modules = {
    module_name: sys.modules.get(module_name)
    for module_name in _STUBBED_MODULES
}

sys.modules.update(_STUBBED_MODULES)
open_kiosco_ready = importlib.import_module("features.open_kiosco_ready")

for module_name, original_module in _original_modules.items():
    if original_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = original_module

features_package = sys.modules.get("features")

if features_package is not None:
    for feature_name in (
        "applications",
        "manual_cancel_last_transation",
        "open_kiosco",
        "out_of_service",
        "payment_screen_close_app",
    ):
        feature_module = getattr(features_package, feature_name, None)
        if feature_module in _STUBBED_MODULES.values():
            delattr(features_package, feature_name)


class OpenKioscoReadyTests(unittest.TestCase):
    @patch("features.open_kiosco_ready.open_kiosco_run")
    def test_opens_kiosco_normally(self, open_kiosco_run_mock):
        open_kiosco_ready.run()

        open_kiosco_run_mock.assert_called_once_with()

    @patch("features.open_kiosco_ready.open_kiosco_run")
    @patch("features.open_kiosco_ready.force_close_kiosk_process")
    @patch("features.open_kiosco_ready.manual_cancel_last_transation_run")
    @patch(
        "features.open_kiosco_ready.is_out_of_service_visible",
        return_value=True,
    )
    @patch("features.open_kiosco_ready.open_anydesk")
    def test_recovers_out_of_service_after_open_failure(
        self,
        open_anydesk_mock,
        is_out_of_service_visible_mock,
        manual_cancel_last_transation_run_mock,
        force_close_kiosk_process_mock,
        open_kiosco_run_mock,
    ):
        open_kiosco_run_mock.side_effect = [RuntimeError("blocked"), None]

        open_kiosco_ready.run()

        self.assertEqual(open_kiosco_run_mock.call_count, 2)
        open_anydesk_mock.assert_called_once_with()
        is_out_of_service_visible_mock.assert_called_once_with(timeout=3)
        manual_cancel_last_transation_run_mock.assert_called_once_with()
        force_close_kiosk_process_mock.assert_called_once_with()

    @patch("features.open_kiosco_ready.open_kiosco_run")
    @patch(
        "features.open_kiosco_ready.is_out_of_service_visible",
        return_value=False,
    )
    @patch("features.open_kiosco_ready.open_anydesk")
    def test_reraises_open_failure_without_out_of_service(
        self,
        _open_anydesk_mock,
        _is_out_of_service_visible_mock,
        open_kiosco_run_mock,
    ):
        open_kiosco_run_mock.side_effect = RuntimeError("not ready")

        with self.assertRaises(RuntimeError):
            open_kiosco_ready.run()


if __name__ == "__main__":
    unittest.main()
