from case_runner import run_stages
from features.kiosk_process import run as kiosk_process_run
from features.login_if_needed import run as login_if_needed_run
from features.magna_amount_100 import run as magna_amount_100_run
from features.open_kiosco_ready import run as open_kiosco_ready_run


# Cierra el kiosco despues de pagar con tarjeta y llegar a instrucciones.
def run():
    return run_stages(
        [
            ("01_open_kiosco", open_kiosco_ready_run),
            ("02_login_if_needed", login_if_needed_run),
            ("03_magna_amount_100_to_instructions", magna_amount_100_run),
            ("04_close_kiosk_at_payment_screen", kiosk_process_run),
            ("05_open_kiosco", open_kiosco_ready_run),
        ]
    )
