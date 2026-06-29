import time

import pyautogui

from features.applications import open_anydesk, open_windows_app
from screenshot import save_screenshot


def run():
    print("Cambiando a WindowsApp para colgar manguera")

    open_windows_app()

    time.sleep(2)

    pyautogui.press("c")  # Colgar

    time.sleep(5)

    save_screenshot("pump_simulator_colgar_after_kiosk_close")

    print("Regresando a AnyDesk")

    open_anydesk()

    save_screenshot("return_anydesk_after_hang_up")
