from detector import find_image
from features.applications import open_anydesk
from features.cancel import run as cancel_run
from features.login_if_needed import run as login_if_needed_run
from features.validate_product_selection import run as validate_product_selection_run
from clicker import click_image
from screenshot import save_screenshot
import time


def is_product_selection_visible(timeout=2):
    return (
        find_image("premium.png", confidence=0.80, timeout=timeout) is not None
        and find_image("magna.png", confidence=0.80, timeout=timeout) is not None
    )


def return_from_intermediate_screen(max_attempts=4):
    for attempt in range(1, max_attempts + 1):
        if is_product_selection_visible(timeout=1):
            return True

        if find_image("regresar_button.png", confidence=0.80, timeout=2) is None:
            return False

        click_image(
            "regresar_button.png",
            timeout=10,
            use_coordinates=False,
            use_region=False,
        )
        time.sleep(1)
        save_screenshot(f"return_to_product_selection_back_{attempt}")

    return is_product_selection_visible(timeout=2)


def run():
    open_anydesk()

    if is_product_selection_visible():
        save_screenshot("product_selection_already_visible")
        return

    if return_from_intermediate_screen():
        save_screenshot("product_selection_after_back")
        return

    if (
        find_image("cancel_service_button.png", confidence=0.80, timeout=3)
        is not None
        or find_image("instructions_title.png", confidence=0.80, timeout=2)
        is not None
    ):
        cancel_run()

    login_if_needed_run()
    validate_product_selection_run()
