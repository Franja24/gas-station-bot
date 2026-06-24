from case_runner import run_stages
from features.invoice import run as invoice_run
from features.login import run as login_run
from features.magna_amount_200 import run as magna_amount_200_run
from features.sevenly_login import run as sevenly_login_run
from features.windows_app import run as windows_run


def run():
    return run_stages(
        [
            ("01_login", login_run),
            ("02_sevenly_login", sevenly_login_run),
            ("03_magna_amount_200", magna_amount_200_run),
            ("04_windows", windows_run),
            ("05_invoice", invoice_run),
        ]
    )
