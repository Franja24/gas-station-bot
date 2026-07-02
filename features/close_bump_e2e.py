from case_runner import run_stages
from features.login import run as login_run
from features.magna import run as magna_run
from features.open_kiosco import run as open_kiosco_run
from features.sevenly_login import run as sevenly_login_run
from features.transaction_cancel_recovery import run as transaction_cancel_recovery_run
from features.windows_app_close_hung_up import run as windows_app_close_hung_up_run
from features.windows_app_hang_up import run as windows_app_hang_up_run


# En este caso se cierra el kiosco cuando la manguera esta descolgada,
# se reabre, se cuelga la manguera, se cancela la transaccion y queda
# lista la pantalla inicial para continuar con el siguiente flujo.
def run():
    return run_stages(
        [
            ("01_open_kiosco", open_kiosco_run),
            ("02_login", login_run),
            ("03_sevenly_login", sevenly_login_run),
            ("04_magna", magna_run),
            ("05_close_app_hose_hung_off", windows_app_close_hung_up_run),
            ("06_open_kiosco", open_kiosco_run),
            ("07_hang_up_hose", windows_app_hang_up_run),
            ("08_cancel_transaction_recovery", transaction_cancel_recovery_run),
        ]
    )
