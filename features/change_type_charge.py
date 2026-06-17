import time

from clicker import ClickError, assert_image_visible, click_image
from features.applications import open_anydesk
from features.premium import handle_benefits_or_payment, wait_for_benefits_or_payment
from screenshot import save_screenshot


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


def click_asset_or_calibrated(image_name, timeout=10):
    try:
        return click_asset(image_name, timeout=timeout)
    except (ClickError, FileNotFoundError) as exc:
        print(
            f"[FALLBACK] {image_name} no se pudo usar por asset: {exc}. "
            "Intentando coordenada calibrada."
        )

        return click_calibrated(image_name, timeout=timeout)


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    # STEP 1 - PREMIUM
    click_asset("premium.png", timeout=10)

    assert_image_visible("amount_1250.png", confidence=0.80, timeout=10)

    save_screenshot("step_1_premium_clicked")

    # STEP 2 - TANQUE LLENO 1250
    click_asset("amount_1250.png", timeout=10)

    assert_image_visible("continue_button.png", confidence=0.80, timeout=10)

    save_screenshot("step_2_full_tank_1250_clicked")

    # STEP 3 - MONTO 500
    click_asset_or_calibrated("charge_type_amount_tab.png", timeout=10)

    time.sleep(1)

    save_screenshot("step_3_amount_tab_clicked")

    click_asset_or_calibrated("charge_amount_500.png", timeout=10)

    time.sleep(1)

    save_screenshot("step_3_1_amount_500_clicked")

    # STEP 4 - LITROS 20
    click_asset_or_calibrated("charge_type_liters_tab.png", timeout=10)

    time.sleep(1)

    save_screenshot("step_4_liters_tab_clicked")

    click_calibrated("charge_liters_20.png", timeout=10)

    assert_image_visible("continue_button.png", confidence=0.80, timeout=10)

    save_screenshot("step_4_1_liters_20_clicked")

    # STEP 5 - CONTINUE
    click_asset("continue_button.png", timeout=10)

    benefits_state = wait_for_benefits_or_payment()

    save_screenshot("step_5_continue_clicked")

    # STEP 6 - BENEFITS OR PAYMENT
    handle_benefits_or_payment(benefits_state)

    # STEP 7 - PAYMENT
    click_asset("card.png", timeout=10)

    save_screenshot("step_7_wait_payment")

    assert_image_visible(
        "payment_success.png",
        confidence=0.80,
        timeout=30,
    )

    save_screenshot("step_7_1_complete_payment")

    save_screenshot("step_8_payment_success")
