import time

import pyautogui

from clicker import assert_image_visible, click_coordinates, click_image
from detector import find_image
from features.applications import (
    WINDOWS_REMOTE_DESKTOP_TITLE,
    open_rustdesk,
    open_windows_app,
)
from screenshot import save_screenshot


def focus_pump_simulator():
    import pygetwindow

    remote_windows = [
        window
        for window in pygetwindow.getAllWindows()
        if WINDOWS_REMOTE_DESKTOP_TITLE.lower() in window.title.lower()
    ]

    if not remote_windows:
        raise RuntimeError("No se encontro la ventana de Escritorio remoto")

    remote_window = remote_windows[0]
    center_x = remote_window.left + remote_window.width // 2
    center_y = remote_window.top + remote_window.height // 2

    print(f"[INFO] Enfocando CSDemo en x={center_x}, y={center_y}")
    click_coordinates(center_x, center_y)
    time.sleep(1)


def get_remote_window():
    import pygetwindow

    remote_windows = [
        window
        for window in pygetwindow.getAllWindows()
        if WINDOWS_REMOTE_DESKTOP_TITLE.lower() in window.title.lower()
    ]

    if not remote_windows:
        raise RuntimeError("No se encontro la ventana de Escritorio remoto")

    return remote_windows[0]


def reset_openpos_pump_to_red():
    remote_window = get_remote_window()

    openpos_title = (
        remote_window.left + 440,
        remote_window.top + 135,
    )
    pump_one_region = (
        remote_window.left + 420,
        remote_window.top + 230,
        160,
        180,
    )
    csdemo_visible_area = (
        remote_window.left + 1200,
        remote_window.top + 500,
    )

    print("[OPENPOS] Llevando OpenPOS al frente")
    click_coordinates(*openpos_title)
    time.sleep(2)

    pump_is_red = find_image(
        "openpos_pump_red.png",
        confidence=0.80,
        timeout=2,
        region=pump_one_region,
    )

    if pump_is_red:
        print("[OPENPOS] La bomba ya esta roja; no es necesario pulsarla")
        save_screenshot("openpos_pump_already_red")
    else:
        assert_image_visible(
            "openpos_pump_green.png",
            confidence=0.80,
            timeout=10,
            region=pump_one_region,
        )
        save_screenshot("openpos_pump_green_visible")

        click_image(
            "openpos_pump_green.png",
            confidence=0.80,
            timeout=10,
            use_coordinates=False,
            use_region=False,
            region=pump_one_region,
        )

    assert_image_visible(
        "openpos_pump_red.png",
        confidence=0.80,
        timeout=10,
        region=pump_one_region,
    )
    save_screenshot("openpos_pump_reset_to_red")

    print("[OPENPOS] Regresando CSDemo al frente")
    click_coordinates(*csdemo_visible_area)
    time.sleep(2)

    assert_image_visible(
        "windows_app_colgada.png",
        confidence=0.80,
        timeout=10,
    )
    save_screenshot("pump_simulator_restored_to_foreground")


def run(reset_openpos_pump=False):
    print("Cambiando a Escritorio remoto para colgar manguera")

    open_windows_app()

    time.sleep(2)

    focus_pump_simulator()

    pyautogui.press("c")  # Colgar

    time.sleep(5)

    assert_image_visible(
        "windows_app_colgada.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("pump_simulator_colgada_validated")

    if reset_openpos_pump:
        reset_openpos_pump_to_red()

    print("Regresando a RustDesk")

    open_rustdesk()

    save_screenshot("return_rustdesk_after_hang_up")
