import time

from clicker import assert_image_visible, click_image
from features.applications import open_anydesk
from screenshot import save_screenshot


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    time.sleep(3)

    click_image("magna.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_1_magna_clicked")

    # STEP 2 - 1250
    click_image("amount_1250.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_2_amount_clicked")

    # STEP 3 - CONTINUE
    click_image("continue_button.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_3_continue_clicked")

    # STEP 4 - PAYMENT
    click_image("card.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_4_wait_payment")

    time.sleep(7)

    save_screenshot("step_4.1_complete_payment")

    time.sleep(2)

    assert_image_visible(
        "payment_success.png",
        confidence=0.80,
        timeout=15,
    )

    save_screenshot("step_5_payment_success")

    save_screenshot("instructions pumb server")
