import time

import pyautogui

from clicker import ClickError
from config.settings import SCREENSHOT_TO_MOUSE_SCALE
from detector import find_image
from screenshot import save_screenshot
from screen_capture import (
    from_target_screen_coordinates,
    get_target_screen_size,
    to_target_screen_coordinates,
)


SETTINGS_BUTTON_ASSET = "settings_button.png"
TRANSACTION_REGISTRY_BUTTON_ASSET = "transaction_registry_button.png"
TRANSACTION_REGISTRY_TITLE_ASSET = "transaction_registry_title.png"
TRANSACTION_SUMMARY_TITLE_ASSET = "transaction_summary_title.png"
BACK_BUTTON_ASSET = "regresar_button.png"

FIRST_TRANSACTION_ROW_OFFSET = (-100, 92)
FIRST_MESSAGE_EYE_OFFSET = (475, 202)
TRANSACTION_REGISTRY_ARROW_OFFSET = (160, 0)


def click_asset(image_name, timeout=10):
    location = find_image(image_name, timeout=timeout)

    if location is None:
        raise ClickError(f"No se encontró el asset requerido: {image_name}.")

    if get_target_screen_size() is None:
        x, y = asset_center_to_local(location)
    else:
        x, y = int(location.x), int(location.y)

    pyautogui.click(x, y)

    return True


def asset_center_to_local(location):
    if get_target_screen_size() is None:
        return (
            int(location.x * SCREENSHOT_TO_MOUSE_SCALE),
            int(location.y * SCREENSHOT_TO_MOUSE_SCALE),
        )

    return from_target_screen_coordinates(
        int(location.x),
        int(location.y),
    )


def find_asset_local_center(image_name, timeout=10):
    location = find_image(image_name, timeout=timeout)

    if location is None:
        raise ClickError(f"No se encontró el asset requerido: {image_name}.")

    return asset_center_to_local(location)


def click_relative_to_asset(image_name, offset, timeout=10):
    x, y = find_asset_local_center(image_name, timeout=timeout)
    offset_x, offset_y = offset

    click_x = x + offset_x
    click_y = y + offset_y

    if get_target_screen_size() is not None:
        global_x, global_y = to_target_screen_coordinates(click_x, click_y)
        pyautogui.click(global_x, global_y)
    else:
        pyautogui.click(click_x, click_y)

    return True


def open_out_of_service_menu():
    pyautogui.press("space")

    time.sleep(1)

    save_screenshot("step_1_out_of_service_menu_opened")


def open_settings():
    click_asset(SETTINGS_BUTTON_ASSET, timeout=15)

    time.sleep(1)

    save_screenshot("step_2_settings_clicked")


def open_transaction_registry():
    click_relative_to_asset(
        TRANSACTION_REGISTRY_BUTTON_ASSET,
        TRANSACTION_REGISTRY_ARROW_OFFSET,
        timeout=15,
    )

    time.sleep(1)

    find_asset_local_center(TRANSACTION_REGISTRY_TITLE_ASSET, timeout=15)

    save_screenshot("step_3_transaction_registry_opened")


def open_first_transaction():
    click_relative_to_asset(
        TRANSACTION_REGISTRY_TITLE_ASSET,
        FIRST_TRANSACTION_ROW_OFFSET,
        timeout=15,
    )

    time.sleep(1)

    find_asset_local_center(TRANSACTION_SUMMARY_TITLE_ASSET, timeout=15)

    save_screenshot("step_4_first_transaction_opened")


def open_first_message_detail():
    click_relative_to_asset(
        TRANSACTION_SUMMARY_TITLE_ASSET,
        FIRST_MESSAGE_EYE_OFFSET,
        timeout=15,
    )

    time.sleep(1)

    save_screenshot("step_5_first_message_eye_clicked")


def go_back():
    click_asset(BACK_BUTTON_ASSET, timeout=10)

    time.sleep(1)

    save_screenshot("step_back_clicked")


def run():
    print("Abriendo ultima operacion para cancelacion")

    open_out_of_service_menu()

    open_settings()

    open_transaction_registry()

    open_first_transaction()

    open_first_message_detail()
