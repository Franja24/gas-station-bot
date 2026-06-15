from case_runner import run_stages
from features.login import run as login_run
from features.open_kiosco import run as open_kiosco_run
from features.premium_close_app import run as premium_close_app_run
from features.windows_app_close_app import run as windows_app_close_run


def run():
    return run_stages(
        [
            ("01_open_kiosco", open_kiosco_run),
            ("02_login", login_run),
            ("03_premium_close_app", premium_close_app_run),
            ("04_windows_app_close", windows_app_close_run),
        ]
    )
