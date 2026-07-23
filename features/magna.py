from clicker import assert_image_visible, click_image
from features.applications import open_anydesk
from features.premium import (
    handle_benefits_or_payment,
    handle_payment_result,
    wait_for_benefits_or_payment,
    wait_for_payment_result,
)
from screenshot import save_screenshot


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    click_asset("magna.png", timeout=10)
    assert_image_visible("amount_1250.png", confidence=0.80, timeout=10)
    save_screenshot("step_1_magna_clicked")

    # STEP 2 - 1250
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

    payment_state = wait_for_payment_result(timeout=30)
    handle_payment_result(payment_state)
    save_screenshot(f"step_6_payment_{payment_state}")
    return payment_state
