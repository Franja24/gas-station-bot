import time
import subprocess

import pyautogui
from clicker import assert_image_visible
from detector import find_image
from features.applications import open_anydesk
from features.premium import (
    click_asset,
    handle_benefits_or_payment,
    wait_for_benefits_or_payment,
)
from features.premium_close_app import close_with_alt_f4
from screenshot import save_screenshot


KIOSK_MARKERS = (
    "card.png",
    "cancel_service_button.png",
    "continue_button.png",
    "dispatch_instructions_title.png",
    "dispatch_step_header.png",
    "iniciar.png",
    "login_button.png",
    "premium.png",
)
FORCE_CLOSE_COMMAND = "taskkill /F /IM pos_build_petro.exe"


def visible_kiosk_markers(timeout=1):
    visible_markers = []

    for marker in KIOSK_MARKERS:
        if find_image(marker, confidence=0.80, timeout=timeout) is not None:
            visible_markers.append(marker)

    return visible_markers


def force_close_kiosk_process():
    print("[CLOSE] Forzando cierre de pos_build_petro.exe en Windows")

    subprocess.run(
        ["pbcopy"],
        input=FORCE_CLOSE_COMMAND,
        text=True,
        check=True,
    )

    time.sleep(1)

    pyautogui.hotkey("command", "r")

    time.sleep(1)

    pyautogui.hotkey("ctrl", "v")

    time.sleep(0.5)

    pyautogui.press("enter")

    time.sleep(5)


def assert_kiosk_closed():
    visible_markers = visible_kiosk_markers(timeout=1)

    if visible_markers:
        raise RuntimeError(
            "El kiosko sigue visible despues del cierre. Marcadores: "
            + ", ".join(visible_markers)
        )

    print("[CLOSE] Kiosko cerrado; no se detectaron marcadores visuales")


def run():
    print("Cerrando kiosko en pantalla de pago")

    open_anydesk()

    # STEP 1 - PREMIUM
    click_asset("premium.png", timeout=10)

    assert_image_visible("amount_1250.png", confidence=0.80, timeout=10)

    save_screenshot("step_1_premium_clicked")

    # STEP 2 - AMOUNT
    click_asset("amount_1250.png", timeout=10)

    assert_image_visible("continue_button.png", confidence=0.80, timeout=10)

    save_screenshot("step_2_amount_clicked")

    # STEP 3 - CONTINUE TO PAYMENT
    click_asset("continue_button.png", timeout=10)

    benefits_state = wait_for_benefits_or_payment()

    save_screenshot("step_3_continue_clicked")

    handle_benefits_or_payment(benefits_state)

    # STEP 4 - PAYMENT SCREEN VISIBLE, BEFORE WINDOWS APP
    assert_image_visible("card.png", confidence=0.80, timeout=10)

    save_screenshot("step_4_payment_screen_visible")

    # STEP 5 - CLICK CARD AND WAIT BEFORE CLOSING
    click_asset("card.png", timeout=10)

    time.sleep(5)

    save_screenshot("step_5_card_clicked_wait_before_close")

    # STEP 6 - CLOSE KIOSK AT PAYMENT SCREEN
    close_with_alt_f4()

    save_screenshot("step_6_alt_f4_close_attempt")

    visible_markers = visible_kiosk_markers(timeout=1)

    if visible_markers:
        print(
            "[CLOSE] Alt+F4 no cerro el kiosko; siguen visibles: "
            + ", ".join(visible_markers)
        )
    else:
        print(
            "[CLOSE] No se detectaron marcadores despues de Alt+F4; "
            "forzando cierre para evitar falsos positivos."
        )

    force_close_kiosk_process()

    save_screenshot("step_7_force_close_attempt")

    assert_kiosk_closed()

    save_screenshot("step_8_kiosk_closed_confirmed")
