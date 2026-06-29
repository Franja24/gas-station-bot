from case_runner import run_stages
from features.login import run as login_run
from features.magna_amount_100 import run as magna_amount_100_run
from features.open_kiosco import run as open_kiosco_run
from features.print_ticket import run as print_ticket_run
from features.sevenly_login import run as sevenly_login_run
from features.windows_app import run as windows_run


def run():
    return run_stages(
        [
            ("00_open_kiosco", open_kiosco_run),
            ("01_login", login_run),
            ("02_sevenly_login", sevenly_login_run),
            ("03_magna_amount_100", magna_amount_100_run),
            ("04_windows", windows_run),
            ("05_print_ticket", print_ticket_run),
        ]
    )
