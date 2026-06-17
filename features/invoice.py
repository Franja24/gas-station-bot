import time
from features.applications import open_anydesk
from clicker import assert_image_visible, click_image
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

    # STEP 1 RETURN TO ANYDESK

    open_anydesk()

    click_asset("invoice.png", timeout=10)

    assert_image_visible("rfc_x.png", confidence=0.80, timeout=10)

    save_screenshot("Step_return_anydesk_invoice_clicked")

    # STEP 2 RFC

    RFC = "XAXX010101000"

    RFC_KEYS = {
        "X": "rfc_x.png",
        "A": "rfc_a.png",
        "0": "rfc_zero.png",
        "1": "rfc_one.png",
    }

    for key in RFC:
        click_asset(RFC_KEYS[key], timeout=10)
        time.sleep(0.5)

    save_screenshot("RFC_clicked")

    # STEP 3 - CONTINUE

    click_asset("continue_button.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_3_continue_clicked")

    time.sleep(2)

    click_asset("continue_button.png", timeout=10)

    assert_image_visible("print.png", confidence=0.80, timeout=15)

    save_screenshot("step_3.1_continue_clicked")


