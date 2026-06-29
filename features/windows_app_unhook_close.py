import time

import pyautogui

from features.applications import open_anydesk, open_windows_app
from features.kiosk_process import force_close_kiosk_process
from features.premium_close_app import close_with_alt_f4
from screenshot import save_screenshot


def run():
    print("Cambiando a WindowsApp")

    open_windows_app()

    time.sleep(2)

    pyautogui.press("d")  # Descolgar

    time.sleep(2)

    save_screenshot("pump_simulator_descolgar_executed")

    print("Cambiando a AnyDesk")

    open_anydesk()

    save_screenshot("return_anydesk")

    close_with_alt_f4()

    save_screenshot("step_2_alt_f4_close_attempt")

    force_close_kiosk_process()

    save_screenshot("step_3_force_close_attempt")
