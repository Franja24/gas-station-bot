import time

import pyautogui

from clicker import assert_image_visible
from detector import find_image
from features.applications import open_anydesk
from features.platform_profile import use_windows_path
from screenshot import save_screenshot


WINDOWS_START_BUTTON_COORDINATES = (960, 718)


def is_product_selection_visible(timeout=2):
    if use_windows_path():
        if (
            find_image(
                "product_selection_windows.png",
                confidence=0.80,
                timeout=timeout,
                confirmations=1,
            )
            is not None
        ):
            return True

    return (
        find_image(
            "premium.png",
            confidence=0.80,
            timeout=timeout,
            confirmations=1,
        ) is not None
        and find_image(
            "magna.png",
            confidence=0.80,
            timeout=timeout,
            confirmations=1,
        ) is not None
    )


def click_start_from_welcome(max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        print(f"[ACTIVE SESSION] Click INICIAR intento {attempt}")

        if use_windows_path():
            pyautogui.click(*WINDOWS_START_BUTTON_COORDINATES)
        else:
            start_asset = find_start_button(timeout=5)

            if start_asset is None:
                start_asset = "start.png"

            location = find_start_button_location(timeout=5)

            if location is None:
                raise RuntimeError(
                    f"No se pudo ubicar el boton de inicio usando {start_asset}"
                )

            pyautogui.click(int(location.x), int(location.y))

        time.sleep(2)

        if is_product_selection_visible(timeout=5):
            return

        save_screenshot(f"start_click_retry_{attempt}")

    if use_windows_path():
        assert_image_visible(
            "product_selection_windows.png",
            confidence=0.80,
            timeout=1,
        )
        return

    assert_image_visible("premium.png", confidence=0.80, timeout=1)
    assert_image_visible("magna.png", confidence=0.80, timeout=1)


def dismiss_windows_start_menu():
    pyautogui.press("esc")
    time.sleep(0.5)


def find_start_button(timeout=10):
    image_candidates = (
        ("start_windows.png", 0.80),
        ("start.png", 0.80),
        ("iniciar.png", 0.85),
    ) if use_windows_path() else (
        ("start.png", 0.80),
        ("iniciar.png", 0.85),
    )

    for image_name, confidence in image_candidates:
        if find_image(image_name, confidence=confidence, timeout=timeout):
            return image_name

    return None


def find_start_button_location(timeout=10, confirmations=2, confidence=0.80):
    image_candidates = (
        ("start_windows_full.png", 0.80),
        ("start_windows_tight.png", 0.80),
        ("start_windows_text.png", 0.80),
        ("start_windows.png", 0.80),
        ("start.png", 0.80),
        ("iniciar.png", 0.85),
    ) if use_windows_path() else (
        ("start.png", 0.80),
        ("iniciar.png", 0.85),
    )

    for image_name, default_confidence in image_candidates:
        location = find_image(
            image_name,
            confidence=confidence if image_name.startswith("start_windows") else default_confidence,
            timeout=timeout,
            confirmations=confirmations,
        )
        if location is not None:
            return location

    return None


def run():
    print("Continuando sesion activa desde pantalla de inicio")

    open_anydesk()
    dismiss_windows_start_menu()

    if is_product_selection_visible(timeout=3):
        print("[ACTIVE SESSION] Seleccion de combustible ya visible")
        save_screenshot("product_selection_already_visible")
        return

    click_start_from_welcome()

    save_screenshot("start_clicked_product_selection_visible")
