import time
from features.applications import open_anydesk
from clicker import click_image_asset
from detector import wait_for_image
from screenshot import save_screenshot, generate_pdf_report


def wait_asset(image_name, confidence, timeout):
    if not wait_for_image(image_name, confidence=confidence, timeout=timeout):
        raise RuntimeError(f"No apareció el asset requerido: {image_name}")


def click_asset(image_name, confidence, timeout):
    if not click_image_asset(
        image_name,
        confidence=confidence,
        timeout=timeout
    ):
        raise RuntimeError(f"No se pudo hacer click por asset: {image_name}")


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    wait_asset("premium.png", confidence=0.35, timeout=15)

    click_asset("premium.png", confidence=0.35, timeout=10)

    wait_asset("amount_1250.png", confidence=0.35, timeout=15)

    save_screenshot("step_1_premium_clicked")

    #STEP 2 - 500
    click_asset("amount_1250.png", confidence=0.35, timeout=10)

    wait_asset("continue_button.png", confidence=0.25, timeout=15)

    save_screenshot("step_2_amount_clicked")

    # STEP 3 - CONTINUE

    click_asset("continue_button.png", confidence=0.25, timeout=10)

    wait_asset("no_benefits_button.png", confidence=0.35, timeout=15)

    save_screenshot("step_3_continue_clicked")

    # STEP 4 - NO BENEFITS

    click_asset("no_benefits_button.png", confidence=0.35, timeout=10)

    wait_asset("card.png", confidence=0.35, timeout=15)

    save_screenshot("step_4_no_benefits_clicked")

    # STEP 5 - PAYMENT

    click_asset("card.png", confidence=0.35, timeout=10)

    save_screenshot("step_5_wait_payment")

    time.sleep(7)

    save_screenshot("step_5.1_complete_payment")

    save_screenshot("instructions pumb server")


    generate_pdf_report()


if __name__ == "__main__":
    run()
