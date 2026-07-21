import time

import pyautogui

from features.applications import open_rustdesk, open_windows_app
from features.kiosk_process import force_close_kiosk_process
from features.windows_app_hang_up_validate import focus_pump_simulator
from screenshot import save_screenshot


def unhook_hose():
    print("Cambiando a WindowsApp")
    # STEP 1 - OPEN WINDOWS APP

    open_windows_app()

    time.sleep(2)

    focus_pump_simulator()

    # STEP 2 - PUMP SIMULATOR

    pyautogui.press("d")   # Descolgar

    print("[PUMP SIMULATOR] Esperando 8 segundos despues de D")
    time.sleep(8)

    save_screenshot("pump_simulator_descolgar_executed")


def start_fuel_dispensing():
    print("[PUMP SIMULATOR] Presionando G para iniciar el surtimiento")
    pyautogui.press("g")   # Gatillo

    time.sleep(30)

    save_screenshot("pump_simulator_gatilo_executed")


def return_to_kiosk_and_close():
    # STEP 4 - RETURN RUSTDESK

    print("Cambiando a RustDesk")

    open_rustdesk()

    save_screenshot("return_rustdesk")

    # STEP 5 - CLOSE APP

    force_close_kiosk_process()

    save_screenshot("step_3_kiosk_closed_once")


def run():
    unhook_hose()
    start_fuel_dispensing()
    return_to_kiosk_and_close()
