from case_runner import run_stages
from features.login_if_needed import run as login_if_needed_run
from features.magna import run as magna_run
from features.open_kiosco_ready import run as open_kiosco_ready_run
from features.windows_app_close_hung_up import run as windows_app_close_hung_up_run


# En este caso se cierra el kiosco cuando la bomba esta colgada
def run():
    return run_stages(
        [
            ("01_open_kiosco", open_kiosco_ready_run),
            ("02_login_if_needed", login_if_needed_run),
            ("03_magna_no_benefits", magna_run),
            ("04_windows", windows_app_close_hung_up_run),
            ("05_open_kiosco", open_kiosco_ready_run),
            ("06_login_if_needed", login_if_needed_run),
        ]
    )
