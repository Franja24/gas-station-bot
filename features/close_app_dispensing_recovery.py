from case_runner import run_stages
from features.magna import run as magna_run
from features.open_kiosco import run as open_kiosco_run
from features.sale_confirmation_recovery import run as sale_confirmation_recovery_run
from features.windows_app_close_app import run as windows_app_close_run


# Parte desde la pantalla inicial Premium/Magna.
def run():
    return run_stages(
        [
            ("01_magna", magna_run),
            ("02_close_app_while_dispensing", windows_app_close_run),
            ("03_open_kiosco", open_kiosco_run),
            ("04_sale_confirmation_recovery", sale_confirmation_recovery_run),
        ]
    )
