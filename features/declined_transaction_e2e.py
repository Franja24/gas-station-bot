import time

from case_runner import run_stages
from clicker import ClickError, assert_image_visible, click_coordinates, click_image
from detector import find_image
from features.applications import open_anydesk
from features.declined_transaction_request import (
    open_declined_request_metadata,
    open_employee_menu,
    open_latest_transaction_summary,
    return_to_product_selection,
)
from features.normal_magna import prepare_product_selection
from features.premium import handle_benefits_or_payment, wait_for_benefits_or_payment
from features.windows_app import run as windows_app_run
from screenshot import save_screenshot


PAYMENT_RESULT = None
FINALIZE_PURCHASE_SUMMARY_COORDINATES = (769, 524)


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def wait_for_payment_result(timeout=30):
    started_at = time.monotonic()

    while time.monotonic() - started_at < timeout:
        if find_image("payment_declined_title.png", confidence=0.80, timeout=1):
            assert_image_visible(
                "payment_declined_message.png",
                confidence=0.80,
                timeout=10,
            )
            return "declined"

        if find_image("dispatch_instructions_title.png", confidence=0.80, timeout=1):
            return "approved"

    raise ClickError("No apareció pago declinado ni instrucciones de despacho.")


def wait_for_final_screen(timeout=30):
    started_at = time.monotonic()

    while time.monotonic() - started_at < timeout:
        if find_image("premium.png", confidence=0.80, timeout=1):
            assert_image_visible("magna.png", confidence=0.80, timeout=10)
            return "product_selection"

        if find_image("start.png", confidence=0.80, timeout=1):
            return "start"

        if find_image("iniciar.png", confidence=0.80, timeout=1):
            return "start"

    raise ClickError("No apareció pantalla final de inicio ni selección.")


def create_magna_payment():
    global PAYMENT_RESULT

    click_asset("magna.png", timeout=10)
    assert_image_visible("amount_1250.png", confidence=0.80, timeout=10)
    save_screenshot("01_magna_clicked")

    click_asset("amount_1250.png", timeout=10)
    assert_image_visible("continue_button.png", confidence=0.80, timeout=10)
    save_screenshot("02_amount_1250_clicked")

    click_asset("continue_button.png", timeout=10)
    benefits_state = wait_for_benefits_or_payment(timeout=20)
    save_screenshot("03_continue_clicked")

    handle_benefits_or_payment(benefits_state)

    click_asset("card.png", timeout=10)
    save_screenshot("04_card_payment_clicked")

    PAYMENT_RESULT = wait_for_payment_result(timeout=30)

    if PAYMENT_RESULT == "declined":
        save_screenshot("05_payment_declined_visible")
        return

    save_screenshot("05_dispatch_instructions_visible")


def complete_approved_dispatch():
    windows_app_run()

    open_anydesk()

    assert_image_visible("purchase_summary_title.png", confidence=0.80, timeout=30)
    click_coordinates(*FINALIZE_PURCHASE_SUMMARY_COORDINATES)

    final_screen = wait_for_final_screen(timeout=30)

    print(f"[APPROVED PAYMENT] Finalizó en pantalla: {final_screen}")
    save_screenshot("06_approved_payment_finalized")


def open_declined_request():
    return_to_product_selection()
    open_employee_menu()
    open_latest_transaction_summary()
    open_declined_request_metadata()


def route_payment_result():
    if PAYMENT_RESULT == "approved":
        complete_approved_dispatch()
        return

    if PAYMENT_RESULT == "declined":
        open_declined_request()
        return

    raise ClickError("No hay resultado de pago para rutear.")


def run():
    global PAYMENT_RESULT

    PAYMENT_RESULT = None

    return run_stages(
        [
            ("01_prepare_product_selection", prepare_product_selection),
            ("02_create_magna_payment", create_magna_payment),
            ("03_route_payment_result", route_payment_result),
        ]
    )
