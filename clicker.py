import time
import pyautogui

from pynput.mouse import Button, Controller
from detector import find_image

mouse = Controller()

SCALE = 0.5


# COORDENADAS CALIBRADAS

COORDS = {
    "start.png": (700, 520),

    "login_button.png": (680, 535),

    "entry_button.png": (650, 500),

    "activate_unit.png": (680,530),

    "amount_500_premium.png": (835, 360),

    "no_benefits_button.png": (650, 450),

    "continue_button.png": (800, 530),

    "card.png": (650, 420),

    "print.png": (700, 460),

    "invoice.png": (800, 340),

    "benefits_telefon_number_button.png": (700, 385)


}

#TECLADO LOGIN
KEYPAD_LOGIN = {

    # FILA NÚMEROS login
    "login_one_button.png":   (490, 350),
    "login_two_button.png":   (520, 350),
    "login_three_button.png": (550, 350),
    "login_four_button.png":  (590, 350),
    "login_five_button.png":  (615, 350),
    "login_six_button.png":   (650, 350),
    "login_seven_button.png": (690, 350),
    "login_eight_button.png": (720, 350),
    "login_nine_button.png":  (750, 350),
    "login_zero_button.png":  (790, 350),

}

# TECLADO NUMÉRICO

KEYPAD_COORDS = {

    # FILA 1
    "one_button.png": (520, 260),
    "two_button.png": (650, 260),
    "three_button.png": (780, 260),

    # FILA 2
    "four_button.png": (520, 340),
    "five_button.png": (650, 340),
    "six_button.png": (780, 340),

    # FILA 3
    "seven_button.png": (520, 400),
    "eight_button.png": (650, 400),
    "nine_button.png": (780, 400),

    # FILA 4
    "zero_button.png": (650, 460),
}

RFC_KEYBOARD_COORDS = {
    "rfc_one.png": (490, 260),
    "rfc_zero.png": (780, 260),
    "rfc_a.png": (490, 380),
    "rfc_x.png": (560, 420),
}

COORDS.update(KEYPAD_COORDS)
COORDS.update(RFC_KEYBOARD_COORDS)
COORDS.update(KEYPAD_LOGIN)


# REGIONES DE BÚSQUEDA

KEYPAD_REGION = (1000, 500, 700, 600)
KEYPAD_LOGIN =  (100, 500, 700, 600)

REGIONS = {
    "premium.png": (900, 300, 600, 400),

    "amount_1250.png": (900, 300, 700, 500),

    "continue_button.png": (900, 550, 800, 450),

    "benefits_telefon_number_button.png": (900, 300, 600, 400),

    "one_button.png": KEYPAD_REGION,
    "two_button.png": KEYPAD_REGION,
    "three_button.png": KEYPAD_REGION,
    "four_button.png": KEYPAD_REGION,
    "five_button.png": KEYPAD_REGION,
    "six_button.png": KEYPAD_REGION,
    "seven_button.png": KEYPAD_REGION,
    "eight_button.png": KEYPAD_REGION,
    "nine_button.png": KEYPAD_REGION,
    "zero_button.png": KEYPAD_REGION,

    "login_one_button": KEYPAD_LOGIN,
    "login_two_button": KEYPAD_LOGIN,
    "login_three_button": KEYPAD_LOGIN,
    "login_four_button": KEYPAD_LOGIN,
    "login_five_button": KEYPAD_LOGIN,
    "login_six_button": KEYPAD_LOGIN
}


# AJUSTES ESPECIALES

SPECIAL_SCALE = {
    "amount_1250.png": (0.62, 0.55),

    "continue_button.png": (0.72, 0.90)
}


def click_image(image_name, confidence=0.45, timeout=10):

    region = REGIONS.get(image_name)

    print(f"[DEBUG] Región usada para {image_name}: {region}")

    location = find_image(
        image_name,
        confidence=confidence,
        timeout=timeout,
        region=region
    )

    if location is None:
        print(f"[ERROR] No se encontró: {image_name}")
        return False

    raw_x = int(location.x)
    raw_y = int(location.y)

    x = int(raw_x * SCALE)
    y = int(raw_y * SCALE)

    # Ajustes especiales

    if image_name in SPECIAL_SCALE:

        scale_x, scale_y = SPECIAL_SCALE[image_name]

        x = int(raw_x * scale_x)
        y = int(raw_y * scale_y)

        print(
            f"[SPECIAL SCALE] {image_name} "
            f"-> x={x}, y={y}"
        )

    print(f"[OK] Detectado {image_name}")
    print(f"Raw: x={raw_x}, y={raw_y}")
    print(f"Click corregido: x={x}, y={y}")

    # Coordenadas calibradas

    if image_name in COORDS:

        x, y = COORDS[image_name]

        print(
            f"[COORDS] {image_name} "
            f"-> x={x}, y={y}"
        )

    print(f"[FINAL] Click en x={x}, y={y}")

    # Mover cursor

    pyautogui.moveTo(x, y, duration=0.5)

    time.sleep(0.5)

    mouse.position = (x, y)

    # Click fuerte

    mouse.press(Button.left)

    time.sleep(0.15)

    mouse.release(Button.left)

    time.sleep(0.15)

    print("[OK] Click fuerte realizado")

    return True

def click_coordinates(x, y):

    print(f"[COORD CLICK] x={x}, y={y}")

    pyautogui.moveTo(x, y, duration=0.5)

    time.sleep(0.5)

    mouse.position = (x, y)

    mouse.press(Button.left)

    time.sleep(0.15)

    mouse.release(Button.left)

    print("[OK] Click por coordenadas realizado")

    return True