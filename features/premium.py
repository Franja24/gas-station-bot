import time
from features.applications import open_anydesk
from clicker import click_image
from screenshot import save_screenshot, generate_pdf_report


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    time.sleep(3)

    click_image("premium.png", confidence=0.35, timeout=10)

    time.sleep(2)

    save_screenshot("step_1_premium_clicked")

    #STEP 2 - 500
    click_image("amount_1250.png", confidence=0.35, timeout=10)

    time.sleep(2)

    save_screenshot("step_2_amount_clicked")

    # STEP 3 - CONTINUE

    click_image("continue_button.png", confidence=0.25, timeout=10)

    time.sleep(2)

    save_screenshot("step_3_continue_clicked")

    # STEP 4 - NO BENEFITS

    click_image("no_benefits_button.png", confidence=0.35, timeout=10)

    time.sleep(2)

    save_screenshot("step_4_no_benefits_clicked")

    # STEP 5 - PAYMENT
    time.sleep(2)

    click_image("card.png", confidence=0.35, timeout=10)

    time.sleep(2)

    save_screenshot("step_5_wait_payment")

    time.sleep(7)

    save_screenshot("step_5.1_complete_payment")

    time.sleep(2)

    save_screenshot("instructions pumb server")


    generate_pdf_report()