import time

import pyautogui

from clicker import assert_image_visible, click_image
from features.applications import open_anydesk
from screenshot import save_screenshot


def click_asset(image_name, timeout=10, use_region=False):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=use_region,
    )


def click_calibrated(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=True,
        use_region=False,
    )


def click_cancel_service():
    try:
        click_asset("cancel_service_button.png", timeout=10)
        return
    except Exception:
        pyautogui.scroll(-5)

        time.sleep(1)

    click_asset("cancel_service_button.png", timeout=10)


def run():
    print("Cancelando servicio")

    open_anydesk()

    click_cancel_service()

    save_screenshot("step_1_cancel_service_clicked")

    assert_image_visible(
        "purchase_summary_title.png",
        confidence=0.80,
        timeout=15,
    )

    save_screenshot("step_2_purchase_summary_visible")

    click_calibrated("finalize_button.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_3_finalize_clicked")

    assert_image_visible(
        "iniciar.png",
        confidence=0.85,
        timeout=15,
    )

    save_screenshot("step_4_start_screen_visible")
