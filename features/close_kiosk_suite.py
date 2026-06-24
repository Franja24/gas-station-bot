from case_runner import run_suite
from features.close_app_e2e import run as close_app_e2e_run
from features.close_bump_e2e import run as close_bump_e2e_run
from features.applications import open_anydesk
from features.manual_cancel_last_transation import (
    run as manual_cancel_last_transation_run,
)
from features.open_kiosco_ready import run as open_kiosco_ready_run
from features.out_of_service import is_out_of_service_visible
from features.payment_screen_close_app import force_close_kiosk_process
from features.payment_screen_close_e2e import run as payment_screen_close_e2e_run


def prepare_close_case():
    open_anydesk()

    if not is_out_of_service_visible(timeout=3):
        return

    print("[SUITE] Bomba fuera de servicio; cancelando ultima transaccion.")

    manual_cancel_last_transation_run()

    force_close_kiosk_process()


def run_payment_screen_close_case():
    prepare_close_case()

    open_kiosco_ready_run()

    return payment_screen_close_e2e_run()


def run_hose_hung_up_case():
    prepare_close_case()

    return close_bump_e2e_run()


def run_fueling_case():
    prepare_close_case()

    return close_app_e2e_run()


def run():
    return run_suite(
        [
            ("01_close_at_payment_screen", run_payment_screen_close_case),
            ("02_close_with_hose_hung_up", run_hose_hung_up_case),
            ("03_close_while_fueling", run_fueling_case),
        ]
    )
