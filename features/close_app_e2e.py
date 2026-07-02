from case_runner import run_stages
from features.close_app_dispensing_recovery import (
    run as close_app_dispensing_recovery_run,
)
from features.login import run as login_run
from features.open_kiosco import run as open_kiosco_run
from features.sevenly_login import run as sevenly_login_run


# En este caso se cierra el kiosco cuando la bomba esta en surtimiento
def run():
    return run_stages(
        [
            ("01_open_kiosco", open_kiosco_run),
            ("02_login", login_run),
            ("03_sevenly_login", sevenly_login_run),
            ("04_close_app_dispensing_recovery", close_app_dispensing_recovery_run),
        ]
    )
