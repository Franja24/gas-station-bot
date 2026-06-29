from case_runner import run_stages
from features.cancel_transaction_session import run as cancel_transaction_session_run
from features.validate_product_selection import run as validate_product_selection_run
from features.windows_app_hang_up_validate import run as windows_app_hang_up_run


def cancel_transaction_without_closing():
    cancel_transaction_session_run(force_close_after=False)


def run():
    return run_stages(
        [
            ("01_cancel_transaction_session", cancel_transaction_without_closing),
            ("02_windows_app_hang_up_validate", windows_app_hang_up_run),
            ("03_validate_product_selection", validate_product_selection_run),
        ]
    )
