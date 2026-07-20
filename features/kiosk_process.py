import subprocess
import time

import pyautogui
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key

from features.applications import open_rustdesk
from features.platform_profile import use_windows_path
from screenshot import save_screenshot


keyboard = KeyboardController()


def _press_remote_hotkey(*keys):
    for key in keys:
        keyboard.press(key)

    time.sleep(0.15)

    for key in reversed(keys):
        keyboard.release(key)


def force_close_kiosk_process():
    print("[CLOSE] Cerrando pos_build_petro en el equipo remoto")

    if use_windows_path():
        width, height = pyautogui.size()
        pyautogui.click(width // 2, height // 2)
        time.sleep(1)

        _press_remote_hotkey(Key.alt, Key.f4)
        time.sleep(4)

        _press_remote_hotkey(Key.cmd, "d")
        time.sleep(3)

        save_screenshot("kiosk_closed_remote_desktop_visible")
        return
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
    open_rustdesk()

    force_close_kiosk_process()

    save_screenshot("kiosk_process_force_close")
