from case_runner import run_stages
from features.confirm_transaction import run as confirm_transaction_run
from features.login_for_confirm_transaction import run as login_for_confirm_run
from features.open_kiosco_ready import run as open_kiosco_ready_run
from features.premium_amount_200 import run as premium_amount_200_run
from features.validate_product_selection import run as validate_product_selection_run
from features.windows_app_close_app import run as windows_app_close_run
from features.windows_app_hang_up_validate import run as windows_app_hang_up_run


def confirm_amount_200_transaction():
    return confirm_transaction_run(expected_amount="200")


def run():
    return run_stages(
        [
            ("01_premium_amount_200_to_instructions", premium_amount_200_run),
            ("02_windows_app_close_while_fueling", windows_app_close_run),
            ("03_windows_app_hang_up_validate", windows_app_hang_up_run),
            ("04_open_kiosco", open_kiosco_ready_run),
            ("05_login_for_confirm", login_for_confirm_run),
            ("06_confirm_transaction", confirm_amount_200_transaction),
            ("07_validate_product_selection", validate_product_selection_run),
        ]
    )
