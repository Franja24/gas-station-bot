from behave import given, then, when

from automation.flows.kiosk_close import kiosk_close_flow


@given("the kiosk application is open and ready")
def step_open_kiosk(context):
    kiosk_close_flow.open_kiosk()


@given("the employee session is active")
def step_employee_session_active(context):
    kiosk_close_flow.ensure_employee_session()


@given("the fuel product selection is visible")
@then("the fuel product selection should be visible")
def step_product_selection_visible(context):
    kiosk_close_flow.validate_product_selection()


@when('I start a "{product}" sale for {amount:d} pesos and reach the payment terminal')
def step_sale_to_payment(context, product, amount):
    kiosk_close_flow.start_sale(product, amount)


@when('I start a "{product}" sale for {amount:d} pesos and wait for payment approval')
def step_sale_waiting_for_approval(context, product, amount):
    kiosk_close_flow.start_sale(product, amount, require_approval=True)


@when('I start a "{product}" sale for {amount:d} pesos and reach the dispatch instructions')
def step_sale_to_dispatch(context, product, amount):
    kiosk_close_flow.start_sale(product, amount, require_approval=True)


@when("I close the kiosk application at the payment screen")
def step_close_at_payment(context):
    kiosk_close_flow.close_kiosk()
    context.kiosk_application_closed = True


@then("the kiosk application should be closed")
def step_kiosk_closed(context):
    if not getattr(context, "kiosk_application_closed", False):
        raise AssertionError("The kiosk close action did not finish")


@when("I reopen the kiosk application")
def step_reopen_kiosk(context):
    kiosk_close_flow.open_kiosk()


@then("the employee login screen should be visible")
def step_employee_login_visible(context):
    kiosk_close_flow.validate_employee_login()


@then("the payment should be approved")
def step_payment_approved(context):
    kiosk_close_flow.require_approved_payment("Magna", 150)


@then("the payment should be approved for the 200 peso sale")
def step_premium_200_payment_approved(context):
    kiosk_close_flow.require_approved_payment("Premium", 200)


@when("I unhook the hose and close the kiosk application")
def step_unhook_and_close(context):
    kiosk_close_flow.unhook_hose_and_close()


@when("I activate the unit for recovery")
def step_activate_unit(context):
    kiosk_close_flow.activate_unit()


@then("the pump out of service screen should be visible")
def step_out_of_service_visible(context):
    kiosk_close_flow.validate_out_of_service()


@when("I cancel the latest transaction for {amount:d} pesos")
def step_cancel_transaction(context, amount):
    kiosk_close_flow.cancel_transaction(amount)


@when("I hang up the hose and reset the OpenPOS pump")
def step_hang_up_and_reset(context):
    kiosk_close_flow.hang_up_and_reset()


@when("I continue the active kiosk session")
def step_continue_session(context):
    kiosk_close_flow.continue_active_session()


@when("I unhook the hose in the pump simulator")
def step_unhook_hose(context):
    kiosk_close_flow.unhook_hose()


@when("I press the trigger to start fuel dispensing")
def step_start_fuel_dispensing(context):
    kiosk_close_flow.start_fuel_dispensing()


@when("I return to the kiosk and close the application")
def step_return_and_close(context):
    kiosk_close_flow.return_to_kiosk_and_close()


@when("I hang up the hose in the pump simulator")
def step_hang_up(context):
    kiosk_close_flow.hang_up_hose()


@when("I log in to recover the pending transaction")
def step_login_for_confirmation(context):
    kiosk_close_flow.login_for_transaction_recovery()


@when("I recover the latest transaction for {amount:d} pesos")
def step_confirm_transaction(context, amount):
    kiosk_close_flow.confirm_transaction(amount)
