import time

from features.applications import open_anydesk
from clicker import ClickError, assert_image_visible, click_image
from detector import find_image
from features.payment_declined_response import run as payment_declined_response_run
from screenshot import save_screenshot


PAYMENT_RESULT_TIMEOUT_SECONDS = 120


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def wait_for_benefits_or_payment(timeout=15):
    start_time = time.monotonic()

    while time.monotonic() - start_time < timeout:
        if find_image("no_benefits_button.png", timeout=1) is not None:
            return "no_benefits"

        if find_image("card.png", timeout=1) is not None:
            return "payment"

    raise ClickError(
        "No apareció no_benefits_button.png ni card.png después de continuar."
    )


def handle_benefits_or_payment(current_state=None):
    state = current_state or wait_for_benefits_or_payment()

    if state == "no_benefits":
        click_asset("no_benefits_button.png", timeout=10)

        assert_image_visible("card.png", confidence=0.80, timeout=10)

        save_screenshot("step_4_no_benefits_clicked")

        return

    if state == "payment":
        print("[PREMIUM] Cliente Sevenly logueado; saltando no benefits")
        save_screenshot("step_4_no_benefits_skipped")

        return

    raise ClickError(
        "No apareció no_benefits_button.png ni card.png después de continuar."
    )


def wait_for_payment_result(timeout=PAYMENT_RESULT_TIMEOUT_SECONDS):
    start_time = time.monotonic()

    while time.monotonic() - start_time < timeout:
        if find_image("payment_success.png", timeout=1) is not None:
            return "success"

        if find_image("payment_declined_title.png", timeout=1) is not None:
            return "declined"

        if find_image(
            "bank_terminal_instructions_title.png",
            timeout=1,
        ) is not None:
            return "ready_for_dispatch"

    raise ClickError(
        "No apareció payment_success.png ni payment_declined_title.png "
        "después de enviar el pago."
    )


def handle_payment_result(current_state=None):
    state = current_state or wait_for_payment_result()

    if state == "success":
        save_screenshot("step_5.1_complete_payment")
        save_screenshot("step_6_payment_success")
        save_screenshot("instructions pumb server")
        return

    if state == "ready_for_dispatch":
        save_screenshot("step_5.1_terminal_ready")
        save_screenshot("instructions_pump_server")
        return

    if state == "declined":
        payment_declined_response_run(open_app=False)
        raise ClickError(
            "Pago declinado; se validó la metadata de respuesta del declinado."
        )

    raise ClickError(
        "Resultado de pago desconocido: "
        f"{state}. Se esperaba success, ready_for_dispatch o declined."
    )


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    click_asset("premium.png", timeout=10)

    assert_image_visible("amount_1250.png", confidence=0.80, timeout=10)

    save_screenshot("step_1_premium_clicked")

    #STEP 2 - 1250
    click_asset("amount_1250.png", timeout=10)

    assert_image_visible("continue_button.png", confidence=0.80, timeout=10)

    save_screenshot("step_2_amount_clicked")

    # STEP 3 - CONTINUE

    click_asset("continue_button.png", timeout=10)

    benefits_state = wait_for_benefits_or_payment()

    save_screenshot("step_3_continue_clicked")

    # STEP 4 - NO BENEFITS

    handle_benefits_or_payment(benefits_state)

    # STEP 5 - PAYMENT
    click_asset("card.png", timeout=10)

    save_screenshot("step_5_wait_payment")

    handle_payment_result(wait_for_payment_result())
