import time

from clicker import assert_image_visible, click_image
from features.applications import open_anydesk
from screenshot import save_screenshot


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
    "9": "nine_button.png",
}

# Las regiones de detección usan pixeles de la captura Retina (2560x1600).
SEVENLY_GREETING_REGION = (1000, 160, 600, 200)


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    time.sleep(3)

    # STEP 1 - SEVENLY
    click_image("sevenly.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_1_sevenly_clicked")

    # STEP 2 - PHONE NUMBER OPTION
    click_image("telefon_number.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_2_telefon_number_clicked")

    # STEP 3 - PHONE NUMBER
    for digit in PHONE_NUMBER:
        click_image(DIGITS[digit], timeout=10)

        time.sleep(2)

    save_screenshot("step_3_phone_number_entered")

    # STEP 4 - CONTINUE
    click_image("continue_button.png", timeout=10)

    time.sleep(4)

    save_screenshot("step_4_continue_clicked")

    # STEP 5 - HOLA CLIENTE
    assert_image_visible("premium.png", confidence=0.80, timeout=15)
    assert_image_visible(
        "sevenly.png",
        confidence=0.80,
        timeout=15,
        region=SEVENLY_GREETING_REGION,
    )

    save_screenshot("step_5_hola_cliente_visible")
