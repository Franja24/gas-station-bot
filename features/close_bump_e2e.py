from case_runner import run_stages
from features.login import run as login_run
from features.magna import run as magna_run
from features.open_kiosco import run as open_kiosco_run
from features.sevenly_login import run as sevenly_login_run
from features.windows_app_close_app import run as windows_close_run


def run():
    return run_stages(
        [
            ("01_login", login_run),
            ("02_sevenly_login", sevenly_login_run),
            ("03_magna", magna_run),
            ("04_windows", windows_close_run),
            ("05_open_kiosco", open_kiosco_run),
        ]
    )
