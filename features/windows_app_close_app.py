import time

import pyautogui

from features.applications import open_anydesk, open_windows_app
from features.kiosk_process import force_close_kiosk_process
from features.premium_close_app import close_with_alt_f4
from screenshot import save_screenshot


def run():
    print("Cambiando a WindowsApp")
    # STEP 1 - OPEN WINDOWS APP

    open_windows_app()

    time.sleep(2)

    # STEP 2 - PUMP SIMULATOR

    pyautogui.press("d")   # Descolgar

    time.sleep(1)

    save_screenshot("pump_simulator_descolgar_executed")

    pyautogui.press("g")   # Gatillo

    time.sleep(30)

    save_screenshot("pump_simulator_gatilo_executed")

    # STEP 4 - RETURN ANYDESK

    print("Cambiando a AnyDesk")

    open_anydesk()

    save_screenshot("return_anydesk")

    # STEP 5 - CLOSE APP

    close_with_alt_f4()

    save_screenshot("step_3_alt_f4_close_attempt")

    force_close_kiosk_process()

    save_screenshot("step_4_force_close_attempt")
