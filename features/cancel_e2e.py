from case_runner import run_stages
from features.login import run as login_run
from features.open_kiosco import run as open_kiosco_run
from features.premium import run as premium_run
from features.cancel import run as cancel_run


def run():
    return run_stages(
        [
            ("01_open_kiosco", open_kiosco_run),
            ("02_login", login_run),
            ("03_premium", premium_run),
            ("04_cancel", cancel_run),
        ]
    )
