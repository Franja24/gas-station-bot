import time

import pyautogui

from clicker import assert_image_visible, click_coordinates, click_image
from detector import find_image
from features.applications import open_anydesk
from screenshot import save_screenshot


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def open_settings_menu():
    pyautogui.press("esc")

    time.sleep(0.5)

    try:
        click_asset("pump_out_of_service_title.png", timeout=3)
    except Exception:
        click_coordinates(500, 200)

    time.sleep(1)

    pyautogui.hotkey("alt", "space")

    time.sleep(0.5)

    pyautogui.press("x")

    time.sleep(2)

    click_coordinates(640, 400)

    time.sleep(0.5)

    pyautogui.press("space")

    time.sleep(2)

    if find_image("employee_settings_button.png", timeout=3) is not None:
        click_asset("employee_settings_button.png", timeout=3)

        time.sleep(2)

    if find_image("employee_settings_button.png", timeout=1) is not None:
        pyautogui.press("left")

        time.sleep(0.2)

        pyautogui.press("enter")

        time.sleep(2)

    if find_image("employee_settings_button.png", timeout=1) is not None:
        pyautogui.press("tab")

        time.sleep(0.2)

        pyautogui.press("tab")

        time.sleep(0.2)

        pyautogui.press("enter")

        time.sleep(2)


def run():
    print("Cancelando manualmente la ultima transaccion")

    open_anydesk()

    # STEP 1 - OPEN HIDDEN SETTINGS MENU
    open_settings_menu()

    assert_image_visible(
        "settings_transaction_log_option.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("step_1_settings_visible")

    # STEP 2 - TRANSACTION LOG
    click_asset("settings_transaction_log_option.png", timeout=10)

    assert_image_visible(
        "transaction_log_title.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("step_2_transaction_log_visible")

    # STEP 3 - OPEN MOST RECENT TRANSACTION
    click_asset("transaction_log_first_row_marker.png", timeout=10)

    assert_image_visible(
        "transaction_summary_title.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("step_3_latest_transaction_visible")

    # STEP 4 - CANCEL TRANSACTION
    click_asset("cancel_transaction_button.png", timeout=10)

    assert_image_visible(
        "confirm_cancel_transaction_button.png",
        confidence=0.80,
        timeout=10,
    )

    time.sleep(3)

    save_screenshot("step_4_cancel_transaction_clicked")

    # STEP 5 - CONFIRM CANCEL TRANSACTION MODAL
    click_asset("confirm_cancel_transaction_button.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_5_cancel_transaction_confirmed")
