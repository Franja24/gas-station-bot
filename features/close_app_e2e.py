from case_runner import run_stages
from features.login import run as login_run
from features.magna import run as magna_run
from features.open_kiosco import run as open_kiosco_run
from features.sevenly_login import run as sevenly_login_run
from features.windows_app_close_app import run as windows_app_close_run


# En este caso se cierra el kiosco cuando la bomba esta colgada.
def run():
    return run_stages(
        [
            ("01_open_kiosco", open_kiosco_run),
            ("02_login", login_run),
            ("03_sevenly_login", sevenly_login_run),
            ("04_magna", magna_run),
            ("05_windows_app_close", windows_app_close_run),
            ("06_open_kiosco", open_kiosco_run),
            ("07_login", login_run),
        ]
    )
