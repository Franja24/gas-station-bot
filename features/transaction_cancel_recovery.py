import time

from clicker import ClickError, assert_image_visible, click_coordinates, click_image
from config.settings import SCREENSHOT_TO_MOUSE_SCALE
from detector import find_image
from features.applications import open_anydesk
from features.login import (
    EMPLOYEE_ID,
    PASSWORD,
    click_asset as click_login_asset,
    click_password_field,
    enter_login_digits,
    get_login_keypad_centers,
    open_login_form,
)
from screenshot import save_screenshot


SETTINGS_BUTTON_OFFSET = (-98, 394)
CONTINUE_SESSION_OFFSET = (9, 394)
FIRST_TRANSACTION_ROW_OFFSET = (0, 105)
CONFIRM_CANCEL_OFFSET = (443, 117)


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def click_relative_to_asset(image_name, offset_x, offset_y, timeout=10):
    location = find_image(image_name, timeout=timeout)

    if location is None:
        raise ClickError(f"No se encontró el ancla {image_name}.")

    x = int((location.x + offset_x) * SCREENSHOT_TO_MOUSE_SCALE)
    y = int((location.y + offset_y) * SCREENSHOT_TO_MOUSE_SCALE)

    print(
        f"[OFFSET CLICK] {image_name} + ({offset_x}, {offset_y}) "
        f"-> x={x}, y={y}"
    )

    return click_coordinates(x, y)


def login_to_employee_menu():
    print("Cambiando a AnyDesk")

    open_anydesk()

    form_location = open_login_form()

    save_screenshot("01_employee_login_start")

    keypad_centers = get_login_keypad_centers(form_location)

    enter_login_digits(EMPLOYEE_ID, keypad_centers)

    click_password_field(form_location)

    time.sleep(1)

    enter_login_digits(PASSWORD, keypad_centers)

    save_screenshot("02_employee_login_completed")

    click_login_asset("entry_button.png")

    assert_image_visible("employee_active_anchor.png", confidence=0.80, timeout=15)

    save_screenshot("03_employee_menu_visible")


def open_transaction_register():
    click_relative_to_asset("employee_active_anchor.png", *SETTINGS_BUTTON_OFFSET)

    assert_image_visible(
        "transaction_register_option.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("04_settings_visible")

    click_asset("transaction_register_option.png", timeout=10)

    assert_image_visible(
        "transaction_register_title.png",
        confidence=0.80,
        timeout=15,
    )

    save_screenshot("05_transaction_register_visible")


def cancel_latest_transaction():
    click_relative_to_asset(
        "transaction_register_title.png",
        *FIRST_TRANSACTION_ROW_OFFSET,
    )

    assert_image_visible(
        "transaction_summary_title.png",
        confidence=0.80,
        timeout=15,
    )

    save_screenshot("06_transaction_summary_visible")

    click_asset("cancel_transaction_button.png", timeout=10)

    assert_image_visible(
        "cancel_transaction_modal_title.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("07_cancel_transaction_modal_visible")

    click_relative_to_asset(
        "cancel_transaction_modal_title.png",
        *CONFIRM_CANCEL_OFFSET,
    )

    assert_image_visible(
        "transaction_register_title.png",
        confidence=0.80,
        timeout=20,
    )

    save_screenshot("08_transaction_cancelled")


def return_to_start_screen():
    click_asset("regresar_button.png", timeout=10)

    assert_image_visible("employee_active_anchor.png", confidence=0.80, timeout=10)

    save_screenshot("09_employee_menu_after_cancel")

    click_relative_to_asset("employee_active_anchor.png", *CONTINUE_SESSION_OFFSET)

    assert_image_visible("premium.png", confidence=0.80, timeout=15)

    save_screenshot("10_start_screen_visible")


def run():
    login_to_employee_menu()
    open_transaction_register()
    cancel_latest_transaction()
    return_to_start_screen()
