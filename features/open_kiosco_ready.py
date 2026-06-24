from features.applications import open_anydesk
from features.manual_cancel_last_transation import (
    run as manual_cancel_last_transation_run,
)
from features.open_kiosco import run as open_kiosco_run
from features.out_of_service import is_out_of_service_visible
from features.payment_screen_close_app import force_close_kiosk_process


def recover_out_of_service_if_visible():
    open_anydesk()

    if not is_out_of_service_visible(timeout=3):
        return False

    print("[OPEN] Bomba fuera de servicio; cancelando ultima transaccion.")

    manual_cancel_last_transation_run()

    force_close_kiosk_process()

    return True


def run():
    try:
        open_kiosco_run()
    except Exception:
        if not recover_out_of_service_if_visible():
            raise

        open_kiosco_run()
