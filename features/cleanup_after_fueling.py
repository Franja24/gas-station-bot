from features.confirm_transaction import run as confirm_transaction_run
from features.validate_out_of_service_or_product_selection import (
    run as validate_final_state_run,
)
from features.windows_app_hang_up_validate import run as windows_app_hang_up_run
from screenshot import save_screenshot


def run():
    try:
        confirm_transaction_run()
    except Exception as exc:
        print(
            "[CLEANUP] No se pudo confirmar transaccion pendiente; "
            f"continuando con colgado y validacion final. Error: {exc}"
        )
        save_screenshot("confirm_transaction_skipped_or_failed")

    windows_app_hang_up_run()
    validate_final_state_run()
