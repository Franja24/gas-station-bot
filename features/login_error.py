import time
from features.applications import open_anydesk
from clicker import assert_image_visible, click_image
from screenshot import save_screenshot


EMPLOYEE_ID = "2"
PASSWORD = "1234567"

LOGIN_DIGITS = {
    "0": "login_zero_button.png",
    "1": "login_one_button.png",
    "2": "login_two_button.png",
    "3": "login_three_button.png",
    "4": "login_four_button.png",
    "5": "login_five_button.png",
    "6": "login_six_button.png",
    "7": "login_seven_button.png",
    "8": "login_eight_button.png",
    "9": "login_nine_button.png",
}


def enter_login_digits(value):
    for digit in value:
        click_image(
            LOGIN_DIGITS[digit],
            timeout=10,
            use_coordinates=False,
            use_region=False,
        )

        time.sleep(1)


def run():

    print("Cambiando a AnyDesk")

    open_anydesk()
    #STEP 1 ID AND PASSWORD

    click_image("login_button.png")

    time.sleep(2)

    save_screenshot("01_login_start")

    # STEP  2 SCREEN LOGIN
    #ID
    enter_login_digits(EMPLOYEE_ID)

    time.sleep(2)

    #  campo de texto password

    click_image(
        "pass_field.png",
        use_coordinates=False,
        use_region=False,
    )

    time.sleep(1)

    # INGRESA PASSWORD
    enter_login_digits(PASSWORD)

    save_screenshot("02_login_completed")

    # STEP  3  LOGIN_BUTTON

    click_image(
        "entry_button.png",
        use_coordinates=False,
        use_region=False,
    )

    time.sleep(2)

    save_screenshot("03_entry button")

    # El login_error solo pasa si aparece la pantalla de error y no inicia sesión.
    assert_image_visible("login_error.png", confidence=0.80, timeout=15)
