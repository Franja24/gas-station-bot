from case_runner import run_stages
from features.confirm_transaction import run as confirm_transaction_run
from features.login_for_confirm_transaction import run as login_for_confirm_run
from features.login_if_needed import run as login_if_needed_run
from features.magna import run as magna_run
from features.open_kiosco_ready import run as open_kiosco_ready_run
from features.validate_product_selection import run as validate_product_selection_run
from features.windows_app_close_app import run as windows_app_close_run
from features.windows_app_hang_up import run as windows_app_hang_up_run


# Cierra el kiosco mientras la bomba esta en surtimiento y confirma la operacion.
def run():
    return run_stages(
        [
            ("01_open_kiosco", open_kiosco_ready_run),
            ("02_login_if_needed", login_if_needed_run),
            ("03_magna_to_instructions", magna_run),
            ("04_windows_app_close", windows_app_close_run),
            ("05_windows_app_hang_up", windows_app_hang_up_run),
            ("06_open_kiosco", open_kiosco_ready_run),
            ("07_login_for_confirm", login_for_confirm_run),
            ("08_confirm_transaction", confirm_transaction_run),
            ("09_validate_product_selection", validate_product_selection_run),
        ]
    )
