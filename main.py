import argparse
import sys

from case_runner import run_case
from features.benefits import run as benefits_run
from features.close_app_e2e import run as close_app_e2e_run
from features.close_bump_e2e import run as close_bump_e2e_run
from features.e2e import run as e2e_run
from features.invoice import run as invoice_run
from features.login import run as login_run
from features.login_error import run as login_error_run
from features.magna import run as magna_run
from features.open_kiosco import run as open_kiosco_run
from features.premium_close_app import run as premium_close_app_run
from features.premium import run as premium_run
from features.sevenly_e2e import run as sevenly_e2e_run
from features.sevenly_login import run as sevenly_login_run
from features.sevenly_login_error import run as sevenly_login_error_run
from features.windows_app import run as windows_run
from features.windows_app_close_app import run as windows_app_close_run
from features.windows_app_close_hung_up import run as windows_app_close_hung_up_run


CASES = {
    "close_app_e2e": close_app_e2e_run,
    "close_bump_e2e": close_bump_e2e_run,
    "e2e": e2e_run,
    "login": login_run,
    "login_error": login_error_run,
    "magna": magna_run,
    "open_kiosco": open_kiosco_run,
    "premium": premium_run,
    "premium_close_app": premium_close_app_run,
    "sevenly_e2e": sevenly_e2e_run,
    "sevenly_login": sevenly_login_run,
    "sevenly_login_error": sevenly_login_error_run,
    "benefits": benefits_run,
    "windows": windows_run,
    "windows_app_close": windows_app_close_run,
    "windows_app_close_hung_up": windows_app_close_hung_up_run,
    "invoice": invoice_run,
}


def parse_args():
    parser = argparse.ArgumentParser(description="Gas Station Automation Bot")
    parser.add_argument(
        "case",
        choices=CASES,
        nargs="?",
        default="e2e",
        help="Caso a ejecutar. El valor predeterminado es e2e.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    success = run_case(args.case, CASES[args.case])

    sys.exit(0 if success else 1)
