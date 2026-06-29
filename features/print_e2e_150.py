from case_runner import run_stages
from features.active_session_start import run as active_session_start_run
from features.magna_amount_150 import run as magna_amount_150_run
from features.print_ticket import run as print_ticket_run
from features.windows_app import run as windows_run


def run():
    return run_stages(
        [
            ("00_active_session_start", active_session_start_run),
            ("01_magna_amount_150", magna_amount_150_run),
            ("02_windows", windows_run),
            ("03_print_ticket", print_ticket_run),
        ]
    )
