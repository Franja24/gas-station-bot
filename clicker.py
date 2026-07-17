import time

import pyautogui
from pynput.mouse import Button, Controller

from config.coordinates import COORDINATES
from config.login_keyboard import LOGIN_KEYBOARD_COORDINATES
from config.phone_keyboard import PHONE_KEYBOARD_COORDINATES
from config.regions import REGIONS
from config.rfc_keyboard import RFC_KEYBOARD_COORDINATES
from config.settings import (
    CLICK_HOLD_SECONDS,
    CLICK_MOVE_DURATION,
    REFERENCE_SCREEN_SIZE,
    SCREENSHOT_TO_MOUSE_SCALE,
)
from detector import find_image
from features.platform_profile import use_windows_path


mouse = Controller()

CALIBRATED_COORDINATES = {
    **COORDINATES,
    **LOGIN_KEYBOARD_COORDINATES,
    **PHONE_KEYBOARD_COORDINATES,
    **RFC_KEYBOARD_COORDINATES,
}


class ClickError(RuntimeError):
    pass


def _validate_calibration():
    current_size = tuple(pyautogui.size())

    if current_size != REFERENCE_SCREEN_SIZE:
        raise ClickError(
            "Las coordenadas fueron calibradas para una pantalla de "
            f"{REFERENCE_SCREEN_SIZE[0]}x{REFERENCE_SCREEN_SIZE[1]}, pero la "
            f"pantalla actual es {current_size[0]}x{current_size[1]}. "
            "Se canceló el clic para evitar un falso positivo."
        )


def click_image(
    image_name,
    confidence=0.80,
    timeout=10,
    use_coordinates=True,
    use_region=True,
    region=None,
):
    search_region = region
    if search_region is None and use_region and not use_windows_path():
        search_region = REGIONS.get(image_name)

    print(
        f"[IMAGE MODE] Buscando {image_name} "
        f"con confianza={confidence:.2f}, región={search_region}"
    )

    location = find_image(
        image_name,
        confidence=confidence,
        timeout=timeout,
        region=search_region,
    )

    if location is None:
        if use_coordinates and image_name in CALIBRATED_COORDINATES:
            x, y = CALIBRATED_COORDINATES[image_name]
            print(
                f"[COORD FALLBACK] No se detectó {image_name}; "
                f"usando x={x}, y={y}"
            )
            return click_coordinates(x, y)

        raise ClickError(
            f"No se encontró una coincidencia segura para {image_name}. "
            "Se canceló el flujo antes de hacer clic."
        )

    x = int(location.x * SCREENSHOT_TO_MOUSE_SCALE)
    y = int(location.y * SCREENSHOT_TO_MOUSE_SCALE)

    print(
        f"[IMAGE MODE] {image_name} detectado en "
        f"x={int(location.x)}, y={int(location.y)}; clic en x={x}, y={y}"
    )

    return click_coordinates(x, y)


def assert_image_visible(image_name, confidence=0.80, timeout=10, region=None):
    print(
        f"[VERIFY] Esperando {image_name} "
        f"con confianza={confidence:.2f}"
    )

    location = find_image(
        image_name,
        confidence=confidence,
        timeout=timeout,
        region=region,
    )

    if location is None:
        raise ClickError(
            f"Validación funcional fallida: no apareció {image_name} "
            f"en {timeout} segundos."
        )

    print(f"[VERIFY] Validación exitosa: {image_name}")

    return True


def click_coordinates(x, y):
    _validate_calibration()

    width, height = REFERENCE_SCREEN_SIZE

    if not 0 <= x < width or not 0 <= y < height:
        raise ClickError(
            f"Coordenada fuera de pantalla: x={x}, y={y}; "
            f"límites={width}x{height}"
        )

    print(f"[COORD CLICK] x={x}, y={y}")

    pyautogui.moveTo(x, y, duration=CLICK_MOVE_DURATION)

    time.sleep(0.5)

    mouse.position = (x, y)
    mouse.press(Button.left)

    time.sleep(CLICK_HOLD_SECONDS)

    mouse.release(Button.left)

    print("[OK] Click por coordenadas realizado")

    return True


def double_click_coordinates(x, y, interval=0.10):
    _validate_calibration()

    width, height = REFERENCE_SCREEN_SIZE

    if not 0 <= x < width or not 0 <= y < height:
        raise ClickError(
            f"Coordenada fuera de pantalla: x={x}, y={y}; "
            f"límites={width}x{height}"
        )

    print(f"[COORD DOUBLE CLICK] x={x}, y={y}")

    pyautogui.moveTo(x, y, duration=CLICK_MOVE_DURATION)

    time.sleep(0.5)

    mouse.position = (x, y)

    for _ in range(2):
        mouse.press(Button.left)

        time.sleep(CLICK_HOLD_SECONDS)

        mouse.release(Button.left)

        time.sleep(interval)

    print("[OK] Doble click por coordenadas realizado")

    return True
