import subprocess
import time

import pyautogui

from features.applications import open_anydesk
from features.platform_profile import use_windows_path
from screenshot import save_screenshot


def force_close_kiosk_process():
    print("[CLOSE] Forzando cierre de pos_build_petro.exe en Windows")

    if use_windows_path():
        pyautogui.hotkey("winleft", "r")
        time.sleep(1)
        pyautogui.write("taskkill /F /IM pos_build_petro.exe", interval=0.01)
    else:
        subprocess.run(
            ["pbcopy"],
            input="taskkill /F /IM pos_build_petro.exe",
            text=True,
            check=True,
        )

        pyautogui.hotkey("command", "r")

        time.sleep(1)

        pyautogui.hotkey("ctrl", "v")

        time.sleep(0.5)

    pyautogui.press("enter")

    time.sleep(5)


def run():
    open_anydesk()

    force_close_kiosk_process()

    save_screenshot("kiosk_process_force_close")
