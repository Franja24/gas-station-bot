import time

from clicker import ClickError, assert_image_visible, click_coordinates, click_image
from config.settings import SCREENSHOT_TO_MOUSE_SCALE
from detector import find_image
from features.applications import open_anydesk
from screenshot import save_screenshot


PHONE_NUMBER = "5531044841"

PHONE_KEYPAD_OFFSETS = {
    "1": (-231, 111),
    "2": (2, 111),
    "3": (235, 111),
    "4": (-231, 227),
    "5": (2, 227),
    "6": (235, 227),
    "7": (-231, 343),
    "8": (2, 343),
    "9": (235, 343),
    "0": (118, 459),
}

# Las regiones de detección usan pixeles de la captura Retina (2560x1600).
SEVENLY_ACCOUNT_REGION = (700, 140, 1000, 240)
SEVENLY_GREETING_REGION = (1000, 160, 600, 200)
SEVENLY_ACCOUNT_FALLBACK_POINTS = [
    (560, 122),
    (500, 122),
    (620, 122),
    (717, 122),
]


def is_sevenly_logged_in(timeout=2):
    return find_image(
        "sevenly_greeting.png",
        timeout=timeout,
        region=SEVENLY_GREETING_REGION,
    ) is not None


def is_phone_option_visible(timeout=2):
    return find_image(
        "telefon_number.png",
        confidence=0.80,
        timeout=timeout,
    ) is not None


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def click_sevenly_account(timeout=25):
    started_at = time.monotonic()
    attempts = 0

    while time.monotonic() - started_at < timeout:
        if is_sevenly_logged_in(timeout=1):
            return

        if is_phone_option_visible(timeout=1):
            save_screenshot("step_1_sevenly_phone_option_visible")
            return

        location = find_image(
            "sevenly.png",
            confidence=0.80,
            timeout=2,
            region=SEVENLY_ACCOUNT_REGION,
        )

        dynamic_points = []
        if location is not None:
            sevenly_x = int(location.x * SCREENSHOT_TO_MOUSE_SCALE)
            sevenly_y = int(location.y * SCREENSHOT_TO_MOUSE_SCALE)
            dynamic_points = [
                (sevenly_x - 160, sevenly_y),
                (sevenly_x - 220, sevenly_y),
                (sevenly_x - 80, sevenly_y),
                (sevenly_x, sevenly_y),
                (sevenly_x + 35, sevenly_y),
            ]

        seen_points = set()
        for point in dynamic_points + SEVENLY_ACCOUNT_FALLBACK_POINTS:
            if point in seen_points:
                continue
            seen_points.add(point)

            attempts += 1
            print(
                "[SEVENLY] Intento "
                f"{attempts}: clic en cuenta Sevenly x={point[0]}, y={point[1]}"
            )
            click_coordinates(*point)
            time.sleep(1.5)

            if is_sevenly_logged_in(timeout=1):
                save_screenshot("step_1_1_sevenly_already_logged_in")
                return

            if is_phone_option_visible(timeout=2):
                save_screenshot("step_1_sevenly_clicked")
                return

    raise ClickError(
        "No se pudo abrir login Sevenly desde el banner superior."
    )


def get_phone_keypad_centers():
    location = find_image("phone_field.png", timeout=10)

    if location is None:
        if find_image("phone_field_filled.png", timeout=2) is not None:
            print("[PHONE KEYPAD MODE] Teléfono ya estaba capturado")
            return None

        raise ClickError(
            "No se encontró el campo de teléfono para calcular el teclado."
        )

    print(
        "[PHONE KEYPAD MODE] Ancla phone_field.png "
        f"en x={int(location.x)}, y={int(location.y)}"
    )

    centers = {}

    for digit, (offset_x, offset_y) in PHONE_KEYPAD_OFFSETS.items():
        raw_x = location.x + offset_x
        raw_y = location.y + offset_y
        centers[digit] = (
            int(raw_x * SCREENSHOT_TO_MOUSE_SCALE),
            int(raw_y * SCREENSHOT_TO_MOUSE_SCALE),
        )

    return centers


def enter_phone_number(phone_number):
    keypad_centers = get_phone_keypad_centers()

    if keypad_centers is None:
        return False

    for digit in phone_number:
        x, y = keypad_centers[digit]
        print(f"[PHONE KEYPAD MODE] Digito {digit} -> x={x}, y={y}")
        click_coordinates(x, y)

        time.sleep(2)

    return True


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    if is_sevenly_logged_in():
        print("[SEVENLY] Cliente ya está logueado")
        save_screenshot("step_0_sevenly_already_logged_in")
        return

    # STEP 1 - SEVENLY
    click_sevenly_account()

    if is_sevenly_logged_in(timeout=3):
        print("[SEVENLY] Cliente ya está logueado")
        save_screenshot("step_1.1_sevenly_already_logged_in")
        return

    assert_image_visible("telefon_number.png", confidence=0.80, timeout=10)

    # STEP 2 - PHONE NUMBER OPTION
    click_asset("telefon_number.png", timeout=10)

    save_screenshot("step_2_telefon_number_clicked")

    # STEP 3 - PHONE NUMBER
    phone_entered = enter_phone_number(PHONE_NUMBER)

    if phone_entered:
        save_screenshot("step_3_phone_number_entered")
    else:
        save_screenshot("step_3_phone_number_already_entered")

    # STEP 4 - CONTINUE
    click_asset("continue_button.png", timeout=10)

    assert_image_visible("premium.png", confidence=0.80, timeout=15)

    save_screenshot("step_4_continue_clicked")

    # STEP 5 - HOLA CLIENTE
    assert_image_visible(
        "sevenly.png",
        confidence=0.80,
        timeout=15,
        region=SEVENLY_GREETING_REGION,
    )

    save_screenshot("step_5_hola_cliente_visible")
