from case_runner import run_stages
from features.activate_unit_for_out_of_service import (
    run as activate_unit_for_out_of_service_run,
)
from features.login_if_needed import run as login_if_needed_run
from features.magna_amount_150 import run as magna_amount_150_run
from features.open_kiosco_ready import run as open_kiosco_ready_run
from features.validate_out_of_service import run as validate_out_of_service_run
from features.windows_app_unhook_close import run as windows_app_unhook_close_run


def run():
    return run_stages(
        [
            ("01_login_if_needed", login_if_needed_run),
            ("02_payment_terminal_ready", magna_amount_150_run),
            ("03_unhook_hose_before_payment_approval", windows_app_unhook_close_run),
            ("04_open_kiosk", open_kiosco_ready_run),
            (
                "05_activate_unit_for_out_of_service",
                activate_unit_for_out_of_service_run,
            ),
            ("06_validate_out_of_service", validate_out_of_service_run),
        ]
    )
