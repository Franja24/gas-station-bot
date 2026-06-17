from clicker import assert_image_visible, click_image
from features.applications import open_anydesk
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
    assert_image_visible("card.png", confidence=0.80, timeout=10)
    save_screenshot("step_3_continue_clicked")

    # STEP 4 - PAYMENT
    click_asset("card.png", timeout=10)
    save_screenshot("step_4_wait_payment")

    assert_image_visible(
        "payment_success.png",
        confidence=0.80,
        timeout=30,
    )

    save_screenshot("step_4.1_complete_payment")
    save_screenshot("step_5_payment_success")
    save_screenshot("instructions pumb server")
