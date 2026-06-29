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
    "0": (638, 433),
    "1": (526, 302),
    "2": (638, 302),
    "3": (752, 302),
    "4": (526, 346),
    "5": (638, 346),
    "6": (752, 346),
    "7": (526, 390),
    "8": (638, 390),
    "9": (752, 390),
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


def click_magna_until_amount_options(max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        print(f"[MAGNA] Intento {attempt} para seleccionar Magna")
        click_asset_or_calibrated("magna.png", timeout=10)

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


def run_amount_payment(amount, flow_name):
    print(f"Cambiando a AnyDesk para pago con monto {amount}")

    open_anydesk()

    # STEP 1 - MAGNA
    click_magna_until_amount_options()

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

    handle_payment_result(wait_for_payment_result())
