import time
from features.applications import open_anydesk

from clicker import click_image
from detector import wait_for_image
from screenshot import save_screenshot, generate_pdf_report



def run():
    print("Cambiando a AnyDesk Tienes 5 segundos...")

    open_anydesk()

    wait_for_image("premium.png", confidence=0.35, timeout=15)


    click_image("premium.png", confidence=0.35, timeout=10)

    wait_for_image("amount_1250.png", confidence=0.35, timeout=15)

    save_screenshot("step_1_premium_clicked")

    #STEP 2 - 500

    click_image("amount_1250.png", confidence=0.35, timeout=10)

    wait_for_image("continue_button.png", confidence=0.25, timeout=15)

    save_screenshot("step_2_amount_clicked")

    # STEP 3 - CONTINUE

    click_image("continue_button.png", confidence=0.25, timeout=10)

    wait_for_image("benefits_telefon_number_button.png", confidence=0.25, timeout=15)

    save_screenshot("step_3_clic_continue_button")

    # STEP 4 - BENEFITS

    click_image("benefits_telefon_number_button.png", confidence=0.25, timeout=10)

    wait_for_image("one_button.png", confidence=0.25, timeout=15)

    save_screenshot("step_4_benefits_clicked")

    #STEP 5 PHONE NUMBER

    PHONE_NUMBER = "5531044841"

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
        "9": "nine_button.png"
    }

    for digit in PHONE_NUMBER:
        click_image(
            DIGITS[digit],
            confidence=0.25,
            timeout=10
        )

    save_screenshot("step_5_benefits_number_clicked")

    click_image("continue_button.png", confidence=0.35, timeout=10)

    time.sleep(4)

    save_screenshot("step_5.1_continue_benefits_number_clicked")

    # STEP 6 - FINAL CONTINUE



    click_image("continue_button.png", confidence=0.35, timeout=10)

    wait_for_image("card.png", confidence=0.35, timeout=20)

    save_screenshot("step_6_continue_final_clicked")

    generate_pdf_report()
