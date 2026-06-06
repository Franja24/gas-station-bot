import time
from features.applications import open_anydesk
from clicker import assert_image_visible, click_coordinates, click_image
from screenshot import save_screenshot


def run():

    print("Cambiando a AnyDesk")

    open_anydesk()

    click_image("login_button.png")

    time.sleep(2)

    save_screenshot("01_login_start")

    # STEP  2 SCREEN LOGIN
    click_image("login_two_button.png")

    time.sleep(2)

    #  campo de texto password

    click_coordinates(660, 310)

    # INGRESA PASSWORD

    time.sleep(1)
    password = [
        "login_one_button.png",
        "login_two_button.png",
        "login_three_button.png",
        "login_four_button.png",
        "login_five_button.png",
        "login_six_button.png"
    ]

    for digit in password:

        click_image(digit, timeout=10)

        time.sleep(1)

    save_screenshot("02_login_completed")

    # STEP  3  LOGIN_BUTTON

    click_image("entry_button.png")

    time.sleep(2)

    save_screenshot("03_entry button")

    # STEP 4 ACTIVATE UNIT

    click_image("activate_unit.png")

    time.sleep(2)

    save_screenshot("04_activate_unit")

    # STEP 5 START

    click_image("start.png")

    time.sleep(2)

    save_screenshot("05_START_unit")

    # El login solo pasa si aparece la pantalla de selección de combustible.
    assert_image_visible("premium.png", confidence=0.80, timeout=15)
