import time

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


def click_calibrated(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=True,
        use_region=False,
    )


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    #Print
    click_asset("print.png", timeout=10)

    save_screenshot("step_1_print_clicked")

    time.sleep(2)

    #finish
    click_calibrated("print_continue_button.png", timeout=10)

    time.sleep(2)

    #Validate case
    assert_image_visible("magna.png", confidence=0.80, timeout=15)

    save_screenshot("step_2_finish_flow")
