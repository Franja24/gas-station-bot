from features.applications import open_anydesk
from clicker import click_image, click_coordinates
from detector import wait_for_image
from screenshot import save_screenshot, generate_pdf_report


def run():

    print("Cambiando a AnyDesk")

    open_anydesk()

    wait_for_image("login_button.png", confidence=0.25, timeout=15)

    click_image("login_button.png", confidence=0.25)

    wait_for_image("login_two_button.png", confidence=0.25, timeout=15)

    save_screenshot("01_login_start")

    # STEP  2 SCREEN LOGIN
    click_image("login_two_button.png", confidence=0.25)

    wait_for_image("login_one_button.png", confidence=0.25, timeout=15)

    #  campo de texto password

    click_coordinates(660, 310)

    # INGRESA PASSWORD

    password = [
        "login_one_button.png",
        "login_two_button.png",
        "login_three_button.png",
        "login_four_button.png",
        "login_five_button.png",
        "login_six_button.png"
    ]

    for digit in password:

        click_image(
            digit,
            confidence=0.45,
            timeout=10
        )

    save_screenshot("02_login_completed")

    # STEP  3  LOGIN_BUTTON

    click_image("entry_button.png", confidence=0.25)

    wait_for_image("activate_unit.png", confidence=0.25, timeout=20)

    save_screenshot("03_entry button")

    # STEP 4 ACTIVATE UNIT

    click_image("activate_unit.png", confidence=0.25)

    wait_for_image("start.png", confidence=0.25, timeout=20)

    save_screenshot("04_activate_unit")

    # STEP 5 START

    click_image("start.png", confidence=0.25)

    wait_for_image("premium.png", confidence=0.35, timeout=20)

    save_screenshot("05_START_unit")

    generate_pdf_report()
