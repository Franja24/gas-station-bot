import time

from clicker import ClickError, assert_image_visible, click_coordinates, click_image
from detector import find_image
from features.applications import open_anydesk
from features.premium import (
    handle_benefits_or_payment,
    handle_payment_result,
    wait_for_benefits_or_payment,
    wait_for_payment_result,
)
from screenshot import save_screenshot


DIGITS = {
    "0": "zero_button.png",
    "1": "one_button.png",
    "2": "two_button.png",
    "3": "three_button.png",
    "4": "four_button.png",
    "5": "five_button.png",
    "6": "six_button.png",
    "7": "seven_button.png",
    "8": "eight_button.png",
    "9": "nine_button.png",
}

AMOUNT_KEYPAD_COORDINATES = {
    # RustDesk en Windows, pantalla local 1920x1200. El kiosco ocupa la
    # columna central y el teclado aparece en x=733..1188, y=427..655.
    "0": (957, 627),
    "1": (806, 453),
    "2": (957, 453),
    "3": (1111, 453),
    "4": (806, 511),
    "5": (957, 511),
    "6": (1111, 511),
    "7": (806, 569),
    "8": (957, 569),
    "9": (1111, 569),
}


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def click_calibrated(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=True,
        use_region=False,
    )


def click_asset_or_calibrated(image_name, timeout=10, use_region=False):
    try:
        return click_image(
            image_name,
            timeout=timeout,
            use_coordinates=False,
            use_region=use_region,
        )
    except (ClickError, FileNotFoundError) as exc:
        print(
            f"[FALLBACK] {image_name} no se pudo usar por asset: {exc}. "
            "Intentando coordenada calibrada."
        )

        return click_calibrated(image_name, timeout=timeout)


def is_visible(image_name, confidence=0.80, timeout=2):
    return find_image(image_name, confidence=confidence, timeout=timeout) is not None


def is_product_selection_visible(timeout=1):
    return (
        is_visible("premium.png", confidence=0.80, timeout=timeout)
        and is_visible("magna.png", confidence=0.80, timeout=timeout)
    )


def click_product_until_amount_options(product="magna", max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        print(f"[PRODUCT] Intento {attempt} para seleccionar {product}")
        click_asset_or_calibrated(f"{product}.png", timeout=10)

        time.sleep(2)

        if is_visible("charge_type_amount_tab.png", confidence=0.80, timeout=3):
            return

        if not is_product_selection_visible(timeout=1):
            return

        save_screenshot(f"magna_selection_retry_{attempt}")

    assert_image_visible("charge_type_amount_tab.png", confidence=0.80, timeout=1)


def enter_amount(amount):
    for digit in str(amount):
        x, y = AMOUNT_KEYPAD_COORDINATES[digit]
        print(f"[AMOUNT KEYPAD MODE] Digito {digit} -> x={x}, y={y}")
        click_coordinates(x, y)

        time.sleep(1)


def open_manual_amount_keypad():
    click_calibrated("charge_amount_input_field.png", timeout=10)

    time.sleep(1)


def wait_for_approved_payment(timeout=120):
    start_time = time.monotonic()

    while time.monotonic() - start_time < timeout:
        if (
            is_visible("payment_success.png", confidence=0.80, timeout=1)
            or is_visible(
                "dispatch_instructions_title.png",
                confidence=0.80,
                timeout=1,
            )
        ):
            save_screenshot("payment_approved_before_opening_pump_simulator")
            return "approved"

        if is_visible("payment_declined_title.png", confidence=0.80, timeout=1):
            assert_image_visible(
                "payment_declined_message.png",
                confidence=0.80,
                timeout=10,
            )
            save_screenshot("payment_declined_before_opening_pump_simulator")
            payment_declined_response_run(open_app=False)
            return "declined"

    raise ClickError(
        "No apareció payment_success.png antes de abrir Escritorio remoto."
    )


def run_amount_payment(
    amount,
    flow_name,
    product="magna",
    require_payment_approval=False,
):
    print(f"Cambiando a RustDesk para pago {product} con monto {amount}")

    open_anydesk()

    # STEP 1 - PRODUCTO
    click_product_until_amount_options(product)

    save_screenshot(f"{flow_name}_step_1_magna_clicked")

    # STEP 3 - MONTO
    click_asset_or_calibrated("charge_type_amount_tab.png", timeout=10)

    time.sleep(1)

    save_screenshot(f"{flow_name}_step_3_amount_tab_clicked")

    open_manual_amount_keypad()

    save_screenshot(f"{flow_name}_step_3_1_amount_field_clicked")

    enter_amount(amount)

    assert_image_visible("continue_button.png", confidence=0.80, timeout=10)

    save_screenshot(f"{flow_name}_step_3_2_amount_{amount}_entered")

    # STEP 4 - CONTINUE
    click_asset("continue_button.png", timeout=10)

    benefits_state = wait_for_benefits_or_payment()

    save_screenshot(f"{flow_name}_step_4_continue_clicked")

    # STEP 5 - BENEFITS OR PAYMENT
    handle_benefits_or_payment(benefits_state)

    assert_image_visible("card.png", confidence=0.80, timeout=10)

    save_screenshot(f"{flow_name}_step_5_payment_visible")

    # STEP 6 - PAYMENT
    click_asset("card.png", timeout=10)

    save_screenshot(f"{flow_name}_step_6_wait_payment")

    payment_state = wait_for_payment_result()
    handle_payment_result(payment_state)

    if require_payment_approval and payment_state == "ready_for_dispatch":
        print("[PAYMENT] Terminal listo; esperando pago aprobado")
        return wait_for_approved_payment()

    return payment_state
