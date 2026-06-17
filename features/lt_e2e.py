from case_runner import run_stages
from features.change_type_charge import run as change_type_charge_run
from features.invoice import run as invoice_run
from features.login import run as login_run
from features.open_kiosco import run as open_kiosco_run
from features.windows_app import run as windows_run


def run():
    return run_stages(
        [
            ("01_open_kiosco", open_kiosco_run),
            ("02_login", login_run),
            ("03_change_type_charge", change_type_charge_run),
            ("04_windows", windows_run),
            ("05_invoice", invoice_run),
        ]
    )
