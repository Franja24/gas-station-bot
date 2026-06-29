from case_runner import run_stages
from features.magna_amount_100 import run as magna_amount_100_run
from features.open_kiosco_ready import run as open_kiosco_ready_run
from features.validate_out_of_service import run as validate_out_of_service_run
from features.windows_app_unhook_close import run as windows_app_unhook_close_run


def run():
    return run_stages(
        [
            ("01_magna_amount_100_to_instructions", magna_amount_100_run),
            ("02_windows_app_unhook_close", windows_app_unhook_close_run),
            ("03_open_kiosco", open_kiosco_ready_run),
            ("04_validate_out_of_service", validate_out_of_service_run),
        ]
    )
