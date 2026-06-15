import time

import pyautogui

from clicker import assert_image_visible, click_image
from features.applications import open_anydesk
from screenshot import save_screenshot


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def close_with_alt_f4():
    pyautogui.hotkey("alt", "f4")

    time.sleep(2)


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    # STEP 1 - PREMIUM
    click_asset("premium.png", timeout=10)

    assert_image_visible("amount_1250.png", confidence=0.80, timeout=10)

    save_screenshot("step_1_premium_clicked")

    # STEP 2 - 1250
    click_asset("amount_1250.png", timeout=10)

    assert_image_visible("continue_button.png", confidence=0.80, timeout=10)

    save_screenshot("step_2_amount_clicked")

    # STEP 3 - CLOSE APP
    close_with_alt_f4()

    save_screenshot("step_3_alt_f4_close_attempt")
