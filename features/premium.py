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


def handle_benefits_or_payment():
    if find_image("no_benefits_button.png", timeout=3) is not None:
        click_asset("no_benefits_button.png", timeout=10)

        time.sleep(2)

        save_screenshot("step_4_no_benefits_clicked")

        return

    if find_image("card.png", timeout=5) is not None:
        print("[PREMIUM] Cliente Sevenly logueado; saltando no benefits")
        save_screenshot("step_4_no_benefits_skipped")

        return

    raise ClickError(
        "No apareció no_benefits_button.png ni card.png después de continuar."
    )


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    time.sleep(3)

    click_asset("premium.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_1_premium_clicked")

    #STEP 2 - 500
    click_asset("amount_1250.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_2_amount_clicked")

    # STEP 3 - CONTINUE

    click_asset("continue_button.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_3_continue_clicked")

    # STEP 4 - NO BENEFITS

    handle_benefits_or_payment()

    # STEP 5 - PAYMENT
    time.sleep(2)

    click_asset("card.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_5_wait_payment")

    time.sleep(7)

    save_screenshot("step_5.1_complete_payment")

    time.sleep(2)

    assert_image_visible(
        "payment_success.png",
        confidence=0.80,
        timeout=15
    )

    save_screenshot("step_6_payment_success")

    save_screenshot("instructions pumb server")
