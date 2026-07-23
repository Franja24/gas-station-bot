import time
from features.applications import open_anydesk
from clicker import assert_image_visible
from features.login import (
    EMPLOYEE_FIELD_OFFSET,
    PASSWORD_FIELD_OFFSET,
    clear_login_field,
    click_asset,
    enter_login_digits,
    get_login_keypad_centers,
    open_login_form,
)
from screenshot import save_screenshot


EMPLOYEE_ID = "2"
PASSWORD = "1234567"

def run(employee_id=EMPLOYEE_ID, password=PASSWORD):

    print("Cambiando a AnyDesk")

    open_anydesk()
    form_location = open_login_form()

    save_screenshot("01_login_start")

    keypad_centers = get_login_keypad_centers(form_location)
    clear_login_field(form_location, EMPLOYEE_FIELD_OFFSET)
    enter_login_digits(employee_id, keypad_centers)

    clear_login_field(form_location, PASSWORD_FIELD_OFFSET)
    enter_login_digits(password, keypad_centers)

    save_screenshot("02_login_completed")

    # STEP  3  LOGIN_BUTTON

    click_asset("entry_button.png")

    time.sleep(2)

    save_screenshot("03_entry button")

    # El login_error solo pasa si aparece la pantalla de error y no inicia sesión.
    assert_image_visible("login_error.png", confidence=0.80, timeout=15)
