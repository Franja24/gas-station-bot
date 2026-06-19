from case_runner import run_suite
from features.cancel_e2e import run as cancel_e2e_run
from features.close_app_e2e import run as close_app_e2e_run
from features.e2e import run as e2e_run
from features.lt_e2e import run as lt_e2e_run
from features.sevenly_e2e import run as sevenly_e2e_run


def run():
    return run_suite(
        [
            ("01_e2e", cancel_e2e_run),
            ("02_sevenly_e2e", sevenly_e2e_run),
            ("03_cancel_e2e", e2e_run),
            ("04_lt_e2e", lt_e2e_run),
            ("05_close_app_e2e", close_app_e2e_run),
        ]
    )
