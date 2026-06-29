import time

import pyautogui

from clicker import assert_image_visible, click_image
from detector import find_image
from features.applications import open_anydesk
from screenshot import save_screenshot


def is_product_selection_visible(timeout=2):
    return (
        find_image("premium.png", confidence=0.80, timeout=timeout) is not None
        and find_image("magna.png", confidence=0.80, timeout=timeout) is not None
    )


def click_start_from_welcome(max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        start_asset = find_start_button(timeout=5)

        if start_asset is None:
            start_asset = "start.png"

        print(f"[ACTIVE SESSION] Click INICIAR intento {attempt}")
        click_image(
            start_asset,
            confidence=0.80,
            timeout=10,
            use_coordinates=False,
            use_region=False,
        )

        time.sleep(2)

        if is_product_selection_visible(timeout=5):
            return

        save_screenshot(f"start_click_retry_{attempt}")

    assert_image_visible("premium.png", confidence=0.80, timeout=1)
    assert_image_visible("magna.png", confidence=0.80, timeout=1)


def dismiss_windows_start_menu():
    pyautogui.press("esc")
    time.sleep(0.5)


def find_start_button(timeout=10):
    for image_name, confidence in (
        ("start.png", 0.80),
        ("iniciar.png", 0.85),
    ):
        if find_image(image_name, confidence=confidence, timeout=timeout):
            return image_name

    return None


def run():
    print("Continuando sesion activa desde pantalla de inicio")

    open_anydesk()
    dismiss_windows_start_menu()

    if is_product_selection_visible(timeout=3):
        print("[ACTIVE SESSION] Seleccion de combustible ya visible")
        save_screenshot("product_selection_already_visible")
        return

    if find_start_button(timeout=15) is None:
        assert_image_visible("iniciar.png", confidence=0.85, timeout=1)

    click_start_from_welcome()

    save_screenshot("start_clicked_product_selection_visible")
