import time

import pyautogui

from features.applications import open_rustdesk, open_windows_app
from features.premium_close_app import close_with_alt_f4
from features.windows_app_hang_up_validate import focus_pump_simulator
from screenshot import save_screenshot


# Cierra el kiosco mientras la manguera queda descolgada.
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

    # STEP 3 - RETURN RUSTDESK

    print("Cambiando a RustDesk")

    open_rustdesk()

    save_screenshot("return_rustdesk")

    # STEP 4 - CLOSE APP WHILE HOSE IS HUNG OFF

    close_with_alt_f4()

    save_screenshot("step_4_alt_f4_close_attempt")
