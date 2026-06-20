import time
from features.applications import open_anydesk
from clicker import ClickError, assert_image_visible, click_coordinates, click_image
from config.settings import SCREENSHOT_TO_MOUSE_SCALE
from detector import find_image
from screenshot import save_screenshot
from screen_capture import from_target_screen_coordinates, get_target_screen_size


EMPLOYEE_ID = "2"
PASSWORD = "123456"

LOGIN_KEYPAD_OFFSETS = {
    "1": (-216, 36),
    "2": (-168, 36),
    "3": (-120, 36),
    "4": (-72, 36),
    "5": (-24, 36),
    "6": (24, 36),
    "7": (72, 36),
    "8": (120, 36),
    "9": (168, 36),
    "0": (216, 36),
}

PASSWORD_FIELD_OFFSET = (122, -18)


def click_asset(image_name, timeout=10, region=None):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
        region=region,
    )


def find_login_form(timeout=10):
    return find_image("login_form_anchor.png", timeout=timeout)


def to_local_form_location(form_location):
    if get_target_screen_size() is None:
        return (
            int(form_location.x * SCREENSHOT_TO_MOUSE_SCALE),
            int(form_location.y * SCREENSHOT_TO_MOUSE_SCALE),
        )

    return from_target_screen_coordinates(
        int(form_location.x),
        int(form_location.y),
    )


def get_login_keypad_centers(form_location):
    if form_location is None:
        raise ClickError(
            "No se encontró el formulario de login para calcular el teclado."
        )

    form_x, form_y = to_local_form_location(form_location)

    print(
        "[KEYPAD MODE] Ancla login_form_anchor.png "
        f"en x={int(form_location.x)}, y={int(form_location.y)}; "
        f"local x={form_x}, y={form_y}"
    )

    centers = {}

    for digit, (offset_x, offset_y) in LOGIN_KEYPAD_OFFSETS.items():
        x = form_x + offset_x
        y = form_y + offset_y
        centers[digit] = (
            int(x),
            int(y),
        )

    return centers


def click_password_field(form_location):
    form_x, form_y = to_local_form_location(form_location)
    offset_x, offset_y = PASSWORD_FIELD_OFFSET
    x = int(form_x + offset_x)
    y = int(form_y + offset_y)

    print(f"[KEYPAD MODE] Campo contraseña -> x={x}, y={y}")
    click_coordinates(x, y)


def enter_login_digits(value, keypad_centers):
    for digit in value:
        x, y = keypad_centers[digit]
        print(f"[KEYPAD MODE] Digito {digit} -> x={x}, y={y}")
        click_coordinates(x, y)

        time.sleep(1)


def open_login_form(max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        form_location = find_login_form(timeout=2)

        if form_location is not None:
            print("[LOGIN] Formulario de usuario y contraseña visible")
            return form_location

        print(f"[LOGIN] Abriendo formulario, intento {attempt}/{max_attempts}")
        click_asset("login_button.png")

        form_location = find_login_form(timeout=5)

        if form_location is not None:
            print("[LOGIN] Formulario de usuario y contraseña visible")
            return form_location

    raise ClickError(
        "No se pudo abrir el formulario de usuario y contraseña."
    )


def run():

    print("Cambiando a AnyDesk")

    open_anydesk()

    form_location = open_login_form()

    save_screenshot("01_login_start")

    keypad_centers = get_login_keypad_centers(form_location)

    # STEP  2 SCREEN LOGIN
    enter_login_digits(EMPLOYEE_ID, keypad_centers)

    #  campo de texto password

    click_password_field(form_location)

    time.sleep(1)

    # INGRESA PASSWORD
    enter_login_digits(PASSWORD, keypad_centers)

    save_screenshot("02_login_completed")

    # STEP  3  LOGIN_BUTTON

    click_asset("entry_button.png")

    assert_image_visible("activate_unit.png", confidence=0.80, timeout=15)

    save_screenshot("03_entry button")

    # STEP 4 ACTIVATE UNIT

    click_asset("activate_unit.png")

    assert_image_visible("start.png", confidence=0.80, timeout=15)

    save_screenshot("04_activate_unit")

    # STEP 5 START

    click_asset("start.png")

    assert_image_visible("premium.png", confidence=0.80, timeout=15)

    save_screenshot("05_START_unit")
