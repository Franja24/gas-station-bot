import argparse
import sys

from case_runner import run_case
from features.benefits import run as benefits_run
from features.cancel import run as cancel_run
from features.cancel_e2e import run as cancel_e2e_run
from features.card_payments_suite import run as card_payments_suite_run
from features.change_type_charge import run as change_type_charge_run
from features.close_app_dispensing_recovery import (
    run as close_app_dispensing_recovery_run,
)
from features.close_app_e2e import run as close_app_e2e_run
from features.close_bump_e2e import run as close_bump_e2e_run
from features.close_kiosk_suite import run as close_kiosk_suite_run
from features.declined_transaction_e2e import run as declined_transaction_e2e_run
from features.declined_transaction_request import (
    run as declined_transaction_request_run,
)
from features.e2e import run as e2e_run
from features.e2e import run_from_start_button as e2e_from_start_button_run
from features.e2e_set_5 import run as e2e_set_5_run
from features.invoice import run as invoice_run
from features.kiosk_process import run as kiosk_process_run
from features.login import run as login_run
from features.login_error import run as login_error_run
from features.lt_e2e import run as lt_e2e_run
from features.magna import run as magna_run
from features.magna_amount_100 import run as magna_amount_100_run
from features.magna_amount_200 import run as magna_amount_200_run
from features.normal_magna import run as normal_magna_run
from features.normal_magna_continue import run as normal_magna_continue_run
from features.open_kiosco import run as open_kiosco_run
from features.payment_declined_response import run as payment_declined_response_run
from features.premium import run as premium_run
from features.premium_close_app import run as premium_close_app_run
from features.print import run as print_run
from features.print_e2e import run as print_e2e_run
from features.print_e2e_150 import run as print_e2e_150_run
from features.print_e2e_suite import run as print_e2e_suite_run
from features.print_ticket import run as print_ticket_run
from features.sale_confirmation_recovery import run as sale_confirmation_recovery_run
from features.sevenly_e2e import run as sevenly_e2e_run
from features.sevenly_login import run as sevenly_login_run
from features.sevenly_login_error import run as sevenly_login_error_run
from features.tdc_e2e import run as tdc_e2e_run
from features.tdc_from_active_session import run as tdc_from_active_session_run
from features.tdc_from_start_screen import run as tdc_from_start_screen_run
from features.tdd_e2e import run as tdd_e2e_run
from features.transaction_cancel_recovery import run as transaction_cancel_recovery_run
from features.unhook_hose_before_payment_approval_e2e import (
    run as unhook_hose_before_payment_approval_run,
)
from features.windows_app import run as windows_run
from features.windows_app_close_app import run as windows_app_close_run
from features.windows_app_close_hung_up import run as windows_app_close_hung_up_run
from features.windows_app_hang_up import run as windows_app_hang_up_run


CASES = {
    "benefits": benefits_run,
    "cancel": cancel_run,
    "cancel_e2e": cancel_e2e_run,
    "card_payments": card_payments_suite_run,
    "card_payments_suite": card_payments_suite_run,
    "change_type_charge": change_type_charge_run,
    "close_app_dispensing_recovery": close_app_dispensing_recovery_run,
    "close_app_e2e": close_app_e2e_run,
    "close_bump_e2e": close_bump_e2e_run,
    "close_kiosk_suite": close_kiosk_suite_run,
    "declined_transaction_e2e": declined_transaction_e2e_run,
    "declined_transaction_request": declined_transaction_request_run,
    "e2e": e2e_run,
    "e2e_start_button": e2e_from_start_button_run,
    "e2e_set_5": e2e_set_5_run,
    "invoice": invoice_run,
    "kios_011": change_type_charge_run,
    "kiosk_process": kiosk_process_run,
    "login": login_run,
    "login_error": login_error_run,
    "lt_e2e": lt_e2e_run,
    "magna": magna_run,
    "magna_amount_100": magna_amount_100_run,
    "magna_amount_200": magna_amount_200_run,
    "normal_magna": normal_magna_run,
    "normal_magna_continue": normal_magna_continue_run,
    "open_kiosco": open_kiosco_run,
    "payment_declined_response": payment_declined_response_run,
    "premium": premium_run,
    "premium_close_app": premium_close_app_run,
    "print": print_run,
    "print_e2e": print_e2e_run,
    "print_e2e_150": print_e2e_150_run,
    "print_e2e_suite": print_e2e_suite_run,
    "print_suite": print_e2e_suite_run,
    "print_ticket": print_ticket_run,
    "sale_confirmation_recovery": sale_confirmation_recovery_run,
    "sevenly_e2e": sevenly_e2e_run,
    "sevenly_login": sevenly_login_run,
    "sevenly_login_error": sevenly_login_error_run,
    "tdc_e2e": tdc_e2e_run,
    "tdc_from_active_session": tdc_from_active_session_run,
    "tdc_from_start_screen": tdc_from_start_screen_run,
    "tdd_e2e": tdd_e2e_run,
    "transaction_cancel_recovery": transaction_cancel_recovery_run,
    "unhook_hose_before_payment_approval": (
        unhook_hose_before_payment_approval_run
    ),
    "windows": windows_run,
    "windows_app_close": windows_app_close_run,
    "windows_app_close_hung_up": windows_app_close_hung_up_run,
    "windows_app_hang_up": windows_app_hang_up_run,
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
