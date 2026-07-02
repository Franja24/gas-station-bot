import time

import pyautogui

from features.applications import open_anydesk, open_windows_app
from screenshot import save_screenshot


def run():
    print("Cambiando a WindowsApp")

    open_windows_app()

    time.sleep(2)

    pyautogui.press("c")   # Colgar

    time.sleep(5)

    save_screenshot("pump_simulator_colgar_executed")

    print("Cambiando a AnyDesk")

    open_anydesk()

    save_screenshot("return_anydesk_after_colgar")
