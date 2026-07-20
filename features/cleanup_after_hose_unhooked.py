from case_runner import run_stages
from features.active_session_start import run as active_session_start_run
from features.cancel_transaction_session import run as cancel_transaction_session_run
from features.magna_amount_150_approved import get_last_payment_result
from features.validate_product_selection import run as validate_product_selection_run
from features.windows_app_hang_up_validate import run as windows_app_hang_up_run


def cancel_transaction_without_closing():
    cancel_transaction_session_run(force_close_after=False, expected_amount="150")


def hang_up_and_reset_openpos_pump():
    windows_app_hang_up_run(reset_openpos_pump=True)


def run():
    if get_last_payment_result() == "declined":
        print(
            "[CLEANUP] Pago declinado ya revisado y pantalla inicial restaurada; "
            "omitiendo clean de manguera."
        )
        return run_stages(
            [("01_validate_product_selection", validate_product_selection_run)]
        )

    return run_stages(
        [
            ("01_cancel_transaction_session", cancel_transaction_without_closing),
            (
                "02_windows_app_hang_up_and_reset_openpos_pump",
                hang_up_and_reset_openpos_pump,
            ),
            ("03_start_active_session", active_session_start_run),
            ("04_validate_product_selection", validate_product_selection_run),
        ]
    )
