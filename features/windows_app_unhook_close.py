import time

import pyautogui

from features.applications import open_rustdesk, open_windows_app
from features.kiosk_process import force_close_kiosk_process
from features.platform_profile import use_windows_path
from features.premium_close_app import close_with_alt_f4
from features.windows_app_hang_up_validate import focus_pump_simulator
from screenshot import save_screenshot


def run():
    print("Cambiando a WindowsApp")

    open_windows_app()

    time.sleep(2)

    focus_pump_simulator()

    pyautogui.press("d")  # Descolgar

    time.sleep(2)

    save_screenshot("pump_simulator_descolgar_executed")

    print("Cambiando a RustDesk")

    open_rustdesk()

    save_screenshot("return_rustdesk")

    if use_windows_path():
        # En Windows, Alt+F4 cerraría la ventana local de RustDesk, no la app
        # pos_build_petro.exe que se ejecuta dentro del equipo remoto.
        print("[CLOSE] Omitiendo Alt+F4 para conservar RustDesk abierto")
    else:
        close_with_alt_f4()
        save_screenshot("step_2_alt_f4_close_attempt")

    force_close_kiosk_process()

    save_screenshot("step_3_force_close_attempt")
