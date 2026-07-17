from case_runner import run_stages
from features.active_session_start import run as active_session_start_run
from features.invoice import run as invoice_run
from features.login import run as login_run
from features.premium import run as premium_run
from features.windows_app import run as windows_run
from features.open_kiosco import run as open_kiosco_run


def run():
    return run_stages(
        [
            ("00_open_kiosco", open_kiosco_run),
            ("01_login", login_run),
            ("02_premium", premium_run),
            ("03_windows", windows_run),
            ("04_print", invoice_run),
        ]
    )


def run_from_start_button():
    return run_stages(
        [
            ("00_start_button", active_session_start_run),
            ("01_login", login_run),
            ("02_premium", premium_run),
            ("03_windows", windows_run),
            ("04_print", invoice_run),
        ]
    )
