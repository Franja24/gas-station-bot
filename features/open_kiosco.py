import subprocess
import time

import pyautogui

from clicker import assert_image_visible, click_image, double_click_coordinates
from config.coordinates import COORDINATES
from detector import find_image
from features.applications import open_anydesk
from screenshot import save_screenshot


PETRO_KIOSK_ICON_COORDINATES = COORDINATES["petro_kiosk_app_icon"]
PETRO_KIOSK_RUN_COMMAND = r'"C:\Program Files\Petro Kiosk App\pos_build_petro.exe"'
REMOTE_WINDOW_CLEANUP_COMMAND = (
    "cmd /c "
    "taskkill /F /IM Taskmgr.exe >nul 2>&1 & "
    "taskkill /F /IM powershell.exe >nul 2>&1 & "
    "taskkill /F /IM WindowsTerminal.exe >nul 2>&1"
)


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


def close_remote_blocking_windows():
    subprocess.run(
        ["pbcopy"],
        input=REMOTE_WINDOW_CLEANUP_COMMAND,
        text=True,
        check=True,
    )

    time.sleep(1)

    pyautogui.hotkey("command", "r")

    time.sleep(2)

    pyautogui.hotkey("ctrl", "v")

    time.sleep(1)

    pyautogui.press("enter")

    time.sleep(3)


def wait_for_login_button(timeout=15):
    return find_image("login_button.png", confidence=0.80, timeout=timeout) is not None


def wait_for_login_form(timeout=2):
    return find_image("login_form_anchor.png", confidence=0.80, timeout=timeout) is not None


def wait_for_product_selection(timeout=2):
    return find_image("premium.png", confidence=0.80, timeout=timeout) is not None


def wait_for_out_of_service(timeout=2):
    return (
        find_image("pump_out_of_service_title.png", confidence=0.80, timeout=timeout)
        is not None
    )


def wait_for_continue_session(timeout=2):
    return (
        find_image("continue_session_button.png", confidence=0.80, timeout=timeout)
        is not None
    )


def wait_for_cancel_service(timeout=2):
    return (
        find_image("cancel_service_button.png", confidence=0.80, timeout=timeout)
        is not None
    )


def wait_for_instructions(timeout=2):
    return (
        find_image("instructions_title.png", confidence=0.80, timeout=timeout)
        is not None
    )


def open_login_screen_from_start(timeout=2):
    if find_image("iniciar.png", confidence=0.85, timeout=timeout) is None:
        return False

    click_image(
        "iniciar.png",
        confidence=0.85,
        timeout=5,
        use_coordinates=False,
        use_region=False,
    )

    time.sleep(2)

    return True


def ensure_login_screen(timeout=15):
    if wait_for_login_button(timeout=timeout):
        return True

    if wait_for_login_form(timeout=2):
        return True

    if wait_for_product_selection(timeout=2):
        return True

    if wait_for_out_of_service(timeout=2):
        return True

    if wait_for_continue_session(timeout=2):
        return True

    if wait_for_cancel_service(timeout=2):
        return True

    if wait_for_instructions(timeout=2):
        return True

    if open_login_screen_from_start(timeout=2):
        return (
            wait_for_login_button(timeout=10)
            or wait_for_login_form(timeout=5)
            or wait_for_product_selection(timeout=5)
            or wait_for_out_of_service(timeout=5)
            or wait_for_continue_session(timeout=5)
            or wait_for_cancel_service(timeout=5)
            or wait_for_instructions(timeout=5)
        )

    return False


def run():
    print("Abriendo Any Desk")

    open_anydesk()

    close_remote_blocking_windows()

    # STEP 1 - OPEN PETRO KIOSK APP FROM WINDOWS RUN
    launch_kiosk_from_run_dialog()

    time.sleep(8)

    save_screenshot("step_1_run_dialog_launch_attempt")

    if ensure_login_screen(timeout=15):
        return

    # Fallback por si Windows no encuentra el acceso directo por ruta.
    show_remote_desktop()

    save_screenshot("step_2_windows_desktop_visible")

    double_click_coordinates(*PETRO_KIOSK_ICON_COORDINATES)

    time.sleep(8)

    save_screenshot("step_3_desktop_icon_launch_attempt")

    # El kiosko esta listo cuando aparece el boton de login.
    if ensure_login_screen(timeout=30):
        return

    assert_image_visible("login_button.png", confidence=0.80, timeout=1)
