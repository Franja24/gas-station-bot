import time
from features.applications import open_anydesk
from clicker import click_image
from screenshot import save_screenshot


def run():
    print("Cambiando a AnyDesk")

    # STEP 1 RETURN TO ANYDESK

    open_anydesk()

    time.sleep(3)

    click_image("invoice.png", timeout=10)

    time.sleep(2)


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
        click_image(RFC_KEYS[key], timeout=10)
        time.sleep(0.5)

    save_screenshot("RFC_clicked")

    # STEP 3 - CONTINUE

    click_image("continue_button.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_3_continue_clicked")

    time.sleep(2)

    click_image("continue_button.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_3.1_continue_clicked")

    # STEP 4 - PRINT/FINISH

    time.sleep(2)

    click_image("print.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_4_print_clicked")
