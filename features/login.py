import time
from features.applications import open_anydesk
from features.platform_profile import use_windows_path
from clicker import ClickError, assert_image_visible, click_coordinates, click_image
from config.settings import SCREENSHOT_TO_MOUSE_SCALE
from detector import find_image
from screenshot import save_screenshot


EMPLOYEE_ID = "2"
PASSWORD = "123456"

WINDOWS_LOGIN_KEYPAD_OFFSETS = {
    "1": (-204, 36),
    "2": (-158, 36),
    "3": (-113, 36),
    "4": (-68, 36),
    "5": (-22, 36),
    "6": (23, 36),
    "7": (68, 36),
    "8": (113, 36),
    "9": (159, 36),
    "0": (204, 36),
}

MAC_LOGIN_KEYPAD_OFFSETS = {
    "1": (-301, 53),
    "2": (-233, 53),
    "3": (-165, 53),
    "4": (-97, 53),
    "5": (-29, 53),
    "6": (39, 53),
    "7": (107, 53),
    "8": (175, 53),
    "9": (243, 53),
    "0": (311, 53),
}

LOGIN_KEYPAD_OFFSETS = (
    WINDOWS_LOGIN_KEYPAD_OFFSETS
    if use_windows_path()
    else MAC_LOGIN_KEYPAD_OFFSETS
)
PASSWORD_FIELD_OFFSET = (115, -15) if use_windows_path() else (172, -28)


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


def find_asset(image_name, timeout=2):
    return find_image(image_name, confidence=0.80, timeout=timeout)


def continue_if_already_authenticated():
    if find_asset("premium.png", timeout=2) is not None:
        print("[LOGIN] Selección de combustible ya visible")
        return True

    if find_asset("start.png", timeout=2) is not None:
        print("[LOGIN] Sesión activa; avanzando desde INICIAR")
        click_asset("start.png")
        assert_image_visible("premium.png", confidence=0.80, timeout=15)
        save_screenshot("00_login_already_authenticated_start")
        return True

    if find_asset("iniciar.png", timeout=2) is not None:
        print("[LOGIN] Sesión activa; avanzando desde INICIAR")
        click_asset("iniciar.png")
        assert_image_visible("premium.png", confidence=0.80, timeout=15)
        save_screenshot("00_login_already_authenticated_iniciar")
        return True

    if find_asset("activate_unit_button.png", timeout=2) is not None:
        print("[LOGIN] Empleado autenticado; activando unidad")
        click_asset("activate_unit_button.png")
        assert_image_visible("start.png", confidence=0.80, timeout=15)
        click_asset("start.png")
        assert_image_visible("premium.png", confidence=0.80, timeout=15)
        save_screenshot("00_login_already_authenticated_activate_unit")
        return True

    return False


def get_login_keypad_centers(form_location):
    if form_location is None:
        raise ClickError(
            "No se encontró el formulario de login para calcular el teclado."
        )

    print(
        "[KEYPAD MODE] Ancla login_form_anchor.png "
        f"en x={int(form_location.x)}, y={int(form_location.y)}"
    )

    centers = {}

    for digit, (offset_x, offset_y) in LOGIN_KEYPAD_OFFSETS.items():
        raw_x = form_location.x + offset_x
        raw_y = form_location.y + offset_y
        centers[digit] = (
            int(raw_x * SCREENSHOT_TO_MOUSE_SCALE),
            int(raw_y * SCREENSHOT_TO_MOUSE_SCALE),
        )

    return centers


def click_password_field(form_location):
    offset_x, offset_y = PASSWORD_FIELD_OFFSET
    x = int((form_location.x + offset_x) * SCREENSHOT_TO_MOUSE_SCALE)
    y = int((form_location.y + offset_y) * SCREENSHOT_TO_MOUSE_SCALE)

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

    if continue_if_already_authenticated():
        return

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

    employee_action = None

    for image_name in (
        "activate_unit_button.png",
        "continue_session_button.png",
    ):
        if find_asset(image_name, timeout=8) is not None:
            employee_action = image_name
            break

    if employee_action is None:
        raise ClickError(
            "Login exitoso, pero no aparecio Activar Unidad ni "
            "Continuar Sesion."
        )

    save_screenshot("03_entry button")

    # STEP 4 ACTIVATE UNIT

    click_asset(employee_action)

    if employee_action == "continue_session_button.png":
        if find_asset("premium.png", timeout=5) is not None:
            save_screenshot("04_continue_session_product_selection")
            return

    assert_image_visible("start.png", confidence=0.80, timeout=15)

    save_screenshot("04_activate_unit")

    # STEP 5 START

    click_asset("start.png")

    assert_image_visible("premium.png", confidence=0.80, timeout=15)

    save_screenshot("05_START_unit")
