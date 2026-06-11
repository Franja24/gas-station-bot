import time
from features.applications import open_anydesk
from clicker import ClickError, assert_image_visible, click_coordinates, click_image
from config.settings import SCREENSHOT_TO_MOUSE_SCALE
from detector import find_image
from screenshot import save_screenshot


EMPLOYEE_ID = "2"
PASSWORD = "123456"

LOGIN_KEYPAD_OFFSETS = {
    "1": (-473, 81),
    "2": (-405, 81),
    "3": (-337, 81),
    "4": (-269, 81),
    "5": (-201, 81),
    "6": (-133, 81),
    "7": (-65, 81),
    "8": (3, 81),
    "9": (71, 81),
    "0": (139, 81),
}


def click_asset(image_name, timeout=10, region=None):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
        region=region,
    )


def get_login_keypad_centers():
    location = find_image("pass_field.png", timeout=10)

    if location is None:
        raise ClickError(
            "No se encontró el campo de contraseña para calcular el teclado."
        )

    print(
        "[KEYPAD MODE] Ancla pass_field.png "
        f"en x={int(location.x)}, y={int(location.y)}"
    )

    centers = {}

    for digit, (offset_x, offset_y) in LOGIN_KEYPAD_OFFSETS.items():
        raw_x = location.x + offset_x
        raw_y = location.y + offset_y
        centers[digit] = (
            int(raw_x * SCREENSHOT_TO_MOUSE_SCALE),
            int(raw_y * SCREENSHOT_TO_MOUSE_SCALE),
        )

    return centers


def enter_login_digits(value, keypad_centers):
    for digit in value:
        x, y = keypad_centers[digit]
        print(f"[KEYPAD MODE] Digito {digit} -> x={x}, y={y}")
        click_coordinates(x, y)

        time.sleep(1)


def run():

    print("Cambiando a AnyDesk")

    open_anydesk()

    click_asset("login_button.png")

    time.sleep(2)

    save_screenshot("01_login_start")

    keypad_centers = get_login_keypad_centers()

    # STEP  2 SCREEN LOGIN
    enter_login_digits(EMPLOYEE_ID, keypad_centers)

    time.sleep(2)

    #  campo de texto password

    click_asset("pass_field.png")

    time.sleep(1)

    # INGRESA PASSWORD
    enter_login_digits(PASSWORD, keypad_centers)

    save_screenshot("02_login_completed")

    # STEP  3  LOGIN_BUTTON

    click_asset("entry_button.png")

    time.sleep(2)

    save_screenshot("03_entry button")

    # STEP 4 ACTIVATE UNIT

    click_asset("activate_unit.png")

    time.sleep(2)

    save_screenshot("04_activate_unit")

    # STEP 5 START

    click_asset("start.png")

    time.sleep(2)

    save_screenshot("05_START_unit")

    # El login solo pasa si aparece la pantalla de selección de combustible.
    assert_image_visible("premium.png", confidence=0.80, timeout=15)
