import time

from clicker import ClickError, assert_image_visible, click_image
from features.applications import open_anydesk
from features.premium import handle_benefits_or_payment, wait_for_benefits_or_payment
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


def enter_amount(amount):
    for digit in str(amount):
        click_asset_or_calibrated(DIGITS[digit], timeout=10, use_region=True)

        time.sleep(1)


def run_amount_payment(amount, flow_name):
    print(f"Cambiando a AnyDesk para pago con monto {amount}")

    open_anydesk()

    # STEP 1 - MAGNA
    click_asset("magna.png", timeout=10)

    assert_image_visible("amount_1250.png", confidence=0.80, timeout=10)

    save_screenshot(f"{flow_name}_step_1_magna_clicked")

    # STEP 2 - TANQUE LLENO
    click_asset("amount_1250.png", timeout=10)

    assert_image_visible("continue_button.png", confidence=0.80, timeout=10)

    save_screenshot(f"{flow_name}_step_2_full_tank_clicked")

    # STEP 3 - MONTO
    click_asset_or_calibrated("charge_type_amount_tab.png", timeout=10)

    time.sleep(1)

    save_screenshot(f"{flow_name}_step_3_amount_tab_clicked")

    enter_amount(amount)

    assert_image_visible("continue_button.png", confidence=0.80, timeout=10)

    save_screenshot(f"{flow_name}_step_3_1_amount_{amount}_entered")

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

    assert_image_visible(
        "payment_success.png",
        confidence=0.80,
        timeout=30,
    )

    save_screenshot(f"{flow_name}_step_6_1_complete_payment")

    save_screenshot(f"{flow_name}_step_7_payment_success")
