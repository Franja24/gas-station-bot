import time

from clicker import assert_image_visible, click_image
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


def is_visible(image_name, confidence=0.80, timeout=2):
    return find_image(image_name, confidence=confidence, timeout=timeout) is not None


def cancel_invoice_if_stuck():
    if not is_visible("cancel_invoice_button.png", confidence=0.80, timeout=2):
        return False

    print("[PRINT TICKET] Pantalla de factura detectada; cancelando factura")
    click_asset("cancel_invoice_button.png", timeout=10)
    assert_image_visible("print_ticket_button.png", confidence=0.80, timeout=10)
    save_screenshot("invoice_cancelled_back_to_summary")

    return True


def is_finished_state():
    return (
        is_visible("start.png", confidence=0.80, timeout=2)
        or is_visible("iniciar.png", confidence=0.85, timeout=2)
        or is_visible("magna.png", confidence=0.80, timeout=2)
    )


def assert_finished_state():
    if is_finished_state():
        return

    assert_image_visible("magna.png", confidence=0.80, timeout=15)


def wait_for_ticket_button_or_finished(timeout=15):
    start_time = time.monotonic()

    while time.monotonic() - start_time < timeout:
        if cancel_invoice_if_stuck():
            if is_visible("print_ticket_button.png", confidence=0.80, timeout=2):
                return "print_ticket"

        if is_visible("print_ticket_button.png", confidence=0.80, timeout=1):
            return "print_ticket"

        if is_finished_state():
            return "finished"

    if is_visible("print_ticket_button.png", confidence=0.80, timeout=1):
        return "print_ticket"

    if is_finished_state():
        return "finished"

    assert_image_visible("print_ticket_button.png", confidence=0.80, timeout=1)

    return "print_ticket"


def run():
    print("Cambiando a AnyDesk para imprimir ticket")

    open_anydesk()

    state = wait_for_ticket_button_or_finished(timeout=15)

    if state == "finished":
        print("[PRINT TICKET] Flujo ya finalizado")
        save_screenshot("print_ticket_already_finished")
        return

    click_asset("print_ticket_button.png", timeout=10)
    save_screenshot("print_ticket_clicked")

    if is_finished_state():
        print("[PRINT TICKET] Flujo finalizado despues de imprimir ticket")
        save_screenshot("print_ticket_finished_after_click")
        return

    if is_visible("finalize_button.png", confidence=0.80, timeout=5):
        click_asset("finalize_button.png", timeout=10)
        save_screenshot("print_ticket_finalize_clicked")

    assert_finished_state()
    save_screenshot("print_ticket_flow_finished")
