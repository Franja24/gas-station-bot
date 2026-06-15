import time

from features.applications import open_anydesk
from clicker import ClickError, assert_image_visible, click_image
from detector import find_image
from screenshot import save_screenshot


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


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    click_asset("premium.png", timeout=10)

    assert_image_visible("amount_1250.png", confidence=0.80, timeout=10)

    save_screenshot("step_1_premium_clicked")

    #STEP 2 - 500
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

    assert_image_visible(
        "payment_success.png",
        confidence=0.80,
        timeout=30
    )

    save_screenshot("step_5.1_complete_payment")

    save_screenshot("step_6_payment_success")

    save_screenshot("instructions pumb server")
