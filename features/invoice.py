import time
from features.applications import open_anydesk
from clicker import click_image
from detector import wait_for_image
from screenshot import save_screenshot, generate_pdf_report


def run():
    print("Cambiando a AnyDesk")

    # STEP 1 RETURN TO ANYDESK

    open_anydesk()

    wait_for_image("invoice.png", confidence=0.35, timeout=15)

    click_image("invoice.png", confidence=0.35, timeout=10)

    wait_for_image("rfc_x.png", confidence=0.25, timeout=15)


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
        click_image(RFC_KEYS[key], confidence=0.25, timeout=10)

    save_screenshot("RFC_clicked")

    # STEP 3 - CONTINUE

    click_image("continue_button.png", confidence=0.25, timeout=10)

    time.sleep(2)

    save_screenshot("step_3_continue_clicked")

    time.sleep(2)

    click_image("continue_button.png", confidence=0.25, timeout=10)

    wait_for_image("print.png", confidence=0.25, timeout=20)

    save_screenshot("step_3.1_continue_clicked")

    # STEP 4 - PRINT/FINISH

    click_image("print.png", confidence=0.25, timeout=10)

    save_screenshot("step_4_print_clicked")
    generate_pdf_report()
