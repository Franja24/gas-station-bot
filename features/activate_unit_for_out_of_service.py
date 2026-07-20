import time

from clicker import assert_image_visible
from detector import find_image
from features.applications import open_rustdesk
from features.login import (
    EMPLOYEE_ID,
    PASSWORD,
    click_asset,
    click_password_field,
    enter_login_digits,
    get_login_keypad_centers,
    open_login_form,
)
from screenshot import save_screenshot


def run():
    print("Autenticando empleado para validar Bomba Fuera de Servicio")
    open_rustdesk()

    if find_image("activate_unit_button.png", timeout=3) is None:
        form_location = open_login_form()
        keypad_centers = get_login_keypad_centers(form_location)

        enter_login_digits(EMPLOYEE_ID, keypad_centers)
        click_password_field(form_location)
        time.sleep(1)
        enter_login_digits(PASSWORD, keypad_centers)

        click_asset("entry_button.png")
        assert_image_visible(
            "activate_unit_button.png",
            confidence=0.80,
            timeout=15,
        )

    save_screenshot("employee_ready_to_activate_unit")
    click_asset("activate_unit_button.png")
    time.sleep(4)
    save_screenshot("unit_activated_for_out_of_service_validation")
