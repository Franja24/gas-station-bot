from case_runner import run_stages
from features.login_if_needed import run as login_if_needed_run
from features.payment_screen_close_app import run as payment_screen_close_app_run
from features.start_kiosk_session import run as start_kiosk_session_run

# from features.open_kiosco import run as open_kiosco_run


def run():
    return run_stages(
        [
            # ("00_open_kiosco", open_kiosco_run),
            ("00_start_kiosk_session", start_kiosk_session_run),
            ("01_login_if_needed", login_if_needed_run),
            ("02_payment_screen_close_app", payment_screen_close_app_run),
        ]
    )
