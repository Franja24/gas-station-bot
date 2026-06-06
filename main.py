import argparse
import sys

from case_runner import run_case
from features.benefits import run as benefits_run
from features.e2e import run as e2e_run
from features.invoice import run as invoice_run
from features.login import run as login_run
from features.magna import run as magna_run
from features.premium import run as premium_run
from features.sevenly_login import run as sevenly_login_run
from features.windows_app import run as windows_run


CASES = {
    "e2e": e2e_run,
    "login": login_run,
    "magna": magna_run,
    "premium": premium_run,
    "sevenly_login": sevenly_login_run,
    "benefits": benefits_run,
    "windows": windows_run,
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
