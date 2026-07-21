from automation.core.validation import (
    employee_login_is_visible,
    require_approved_payment,
)
from automation.flows.sales import start_amount_sale
from automation.screens import kiosk, pump_simulator, transactions


class KioskCloseFlow:
    def __init__(self):
        self._payment_results = {}

    def open_kiosk(self):
        return kiosk.open_kiosk()

    def ensure_employee_session(self):
        return kiosk.ensure_employee_session()

    def validate_product_selection(self):
        return kiosk.validate_product_selection()

    def start_sale(self, product, amount, *, require_approval=False):
        result = start_amount_sale(
            product,
            amount,
            require_payment_approval=require_approval,
        )
        self._payment_results[(product.lower(), int(amount))] = result
        return result

    def require_approved_payment(self, product, amount):
        key = (product.lower(), int(amount))
        require_approved_payment(
            self._payment_results.get(key),
            f"{product} {amount}",
        )

    def close_kiosk(self):
        return kiosk.close_kiosk()

    def validate_employee_login(self):
        return employee_login_is_visible()

    def unhook_hose_and_close(self):
        return pump_simulator.unhook_hose_and_close()

    def activate_unit(self):
        return kiosk.activate_unit()

    def validate_out_of_service(self):
        return kiosk.validate_out_of_service()

    def cancel_transaction(self, amount):
        return transactions.cancel_transaction(
            force_close_after=False,
            expected_amount=str(amount),
        )

    def hang_up_and_reset(self):
        return pump_simulator.hang_up_hose(reset_openpos_pump=True)

    def continue_active_session(self):
        return kiosk.continue_active_session()

    def unhook_hose(self):
        return pump_simulator.unhook_hose()

    def start_fuel_dispensing(self):
        return pump_simulator.start_fuel_dispensing()

    def return_to_kiosk_and_close(self):
        return pump_simulator.return_to_kiosk_and_close()

    def hang_up_hose(self):
        return pump_simulator.hang_up_hose()

    def login_for_transaction_recovery(self):
        return kiosk.login_for_confirmation()

    def confirm_transaction(self, amount):
        return transactions.confirm_transaction(expected_amount=str(amount))


kiosk_close_flow = KioskCloseFlow()
