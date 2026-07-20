import time

import pyautogui

from features.applications import open_rustdesk, open_windows_app
from features.kiosk_process import force_close_kiosk_process
from features.windows_app_hang_up_validate import focus_pump_simulator
from screenshot import save_screenshot


def run():
    print("Cambiando a WindowsApp")
    # STEP 1 - OPEN WINDOWS APP

    open_windows_app()

    time.sleep(2)

    focus_pump_simulator()

    # STEP 2 - PUMP SIMULATOR

    pyautogui.press("d")   # Descolgar

    time.sleep(1)

    save_screenshot("pump_simulator_descolgar_executed")

    pyautogui.press("g")   # Gatillo

    time.sleep(30)

    save_screenshot("pump_simulator_gatilo_executed")

    # STEP 4 - RETURN RUSTDESK

    print("Cambiando a RustDesk")

    open_rustdesk()

    save_screenshot("return_rustdesk")

    # STEP 5 - CLOSE APP

    force_close_kiosk_process()

    save_screenshot("step_3_kiosk_closed_once")
