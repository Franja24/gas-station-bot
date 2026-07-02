import subprocess
import time

import pyautogui

from clicker import assert_image_visible, double_click_coordinates
from config.coordinates import COORDINATES
from detector import find_image
from features.applications import open_anydesk
from screenshot import save_screenshot


PETRO_KIOSK_ICON_COORDINATES = COORDINATES["petro_kiosk_app_icon"]
PETRO_KIOSK_RUN_COMMAND = r'"C:\Program Files\Petro Kiosk App\pos_build_petro.exe"'


def show_remote_desktop():
    pyautogui.hotkey("command", "d")

    time.sleep(2)


def launch_kiosk_from_run_dialog():
    subprocess.run(
        ["pbcopy"],
        input=PETRO_KIOSK_RUN_COMMAND,
        text=True,
        check=True,
    )

    time.sleep(1)

    pyautogui.hotkey("command", "r")

    time.sleep(2)

    pyautogui.hotkey("ctrl", "v")

    time.sleep(1)

    pyautogui.press("enter")


def is_kiosk_ready(timeout=3):
    ready_assets = (
        "login_button.png",
        "start.png",
        "iniciar.png",
        "purchase_summary_title.png",
        "premium.png",
        "magna.png",
        "amount_1250.png",
    )
    for asset in ready_assets:
        if find_image(asset, confidence=0.80, timeout=timeout) is not None:
            print(f"[OK] Kiosko listo con asset: {asset}")
            return True
    return False


def run():
    print("Abriendo Any Desk")

    open_anydesk()

    if is_kiosk_ready(timeout=2):
        save_screenshot("step_0_kiosk_already_ready")
        return

    # STEP 1 - OPEN PETRO KIOSK APP FROM WINDOWS RUN
    launch_kiosk_from_run_dialog()

    time.sleep(8)

    save_screenshot("step_1_run_dialog_launch_attempt")

    if not is_kiosk_ready(timeout=15):
        # Fallback por si Windows no encuentra el acceso directo por ruta.
        show_remote_desktop()

        save_screenshot("step_2_windows_desktop_visible")

        double_click_coordinates(*PETRO_KIOSK_ICON_COORDINATES)

        time.sleep(8)

        save_screenshot("step_3_desktop_icon_launch_attempt")

    if not is_kiosk_ready(timeout=30):
        assert_image_visible("login_button.png", confidence=0.80, timeout=1)
