import time

from clicker import assert_image_visible, click_image
from detector import find_image
from features.applications import open_anydesk
from features.print import run as print_run
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


def is_visible(image_name, confidence=0.80, timeout=2):
    return find_image(image_name, confidence=confidence, timeout=timeout) is not None


def enter_rfc():
    rfc = "XAXX010101000"
    rfc_keys = {
        "X": "rfc_x.png",
        "A": "rfc_a.png",
        "0": "rfc_zero.png",
        "1": "rfc_one.png",
    }

    for key in rfc:
        click_asset(rfc_keys[key], timeout=10)
        time.sleep(0.5)

    save_screenshot("RFC_clicked")


def cancel_invoice_if_stuck():
    if not is_visible("cancel_invoice_button.png", confidence=0.80, timeout=2):
        return False

    print("[INVOICE] Factura atorada; cancelando factura")
    click_asset("cancel_invoice_button.png", timeout=10)
    assert_image_visible("print_ticket_button.png", confidence=0.80, timeout=10)
    save_screenshot("invoice_cancelled_back_to_summary")

    return True


def click_continue_until_print(max_attempts=4):
    for attempt in range(1, max_attempts + 1):
        click_asset("continue_button.png", timeout=10)
        time.sleep(2)
        save_screenshot(f"continue_to_print_attempt_{attempt}")

        if is_visible("print.png", confidence=0.80, timeout=5):
            return True

        if cancel_invoice_if_stuck():
            return False

    assert_image_visible("print.png", confidence=0.80, timeout=1)
    return True


def run(submit_print=False):
    print("Cambiando a AnyDesk")

    open_anydesk()

    if cancel_invoice_if_stuck():
        return

    if is_visible("invoice.png", confidence=0.80, timeout=3):
        click_asset("invoice.png", timeout=10)
        assert_image_visible("rfc_x.png", confidence=0.80, timeout=10)
        save_screenshot("Step_return_anydesk_invoice_clicked")

    if is_visible("rfc_x.png", confidence=0.80, timeout=3):
        enter_rfc()

    if not click_continue_until_print():
        return

    save_screenshot("step_3.1_continue_clicked")

    if submit_print:
        print_run()
        return

    click_calibrated("invoice_continue_button.png", timeout=10)
    assert_image_visible("magna.png", confidence=0.80, timeout=15)
    save_screenshot("step_4_Finsh flow")
