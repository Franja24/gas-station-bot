import time

from clicker import ClickError, assert_image_visible, click_coordinates, click_image
from config.phone_keyboard import PHONE_KEYBOARD_COORDINATES
from detector import find_image
from features.active_session_start import run as active_session_start_run
from features.applications import open_anydesk
from features.kiosk_process import force_close_kiosk_process
from screenshot import save_screenshot


def close_kiosk_after_checkpoint():
    print("[CLEANUP] Cerrando kiosco despues del checkpoint de beneficios")
    force_close_kiosk_process()
    save_screenshot("step_7_kiosk_closed_after_benefits")



def run():
    print("Preparando sesion activa desde la pantalla INICIAR...")

    open_anydesk()
    if find_image("dispatch_instructions_title.png", timeout=3) is not None:
        print("[BENEFITS] Checkpoint Sevenly ya completado en despacho")
        save_screenshot("benefits_dispatch_already_visible")
        close_kiosk_after_checkpoint()
        return

    phone_screen_visible = (
        find_image("phone_field.png", timeout=3) is not None
        or find_image("phone_field_filled.png", timeout=2) is not None
        or find_image("one_button.png", timeout=2) is not None
        or find_image("continue_button.png", timeout=2) is not None
    )

    if phone_screen_visible:
        print("[BENEFITS] Reanudando desde el teclado de telefono")
    else:
        active_session_start_run()

        click_image("premium.png", timeout=10)
        time.sleep(2)
        save_screenshot("step_1_premium_clicked")

        click_image("amount_1250.png", timeout=10)
        time.sleep(2)
        save_screenshot("step_2_amount_clicked")

        click_image("continue_button.png", timeout=10)
        time.sleep(2)
        save_screenshot("step_3_clic_continue_button")

        click_image("benefits_telefon_number_button.png", timeout=10)
        time.sleep(2)
        save_screenshot("step_4_benefits_clicked")

    #STEP 5 PHONE NUMBER

    PHONE_NUMBER = "5531044841"

    DIGITS = {
        "0": "zero_button.png",
        "1": "one_button.png",
        "2": "two_button.png",
        "3": "three_button.png",
        "4": "four_button.png",
        "5": "five_button.png",
        "6": "six_button.png",
        "7": "seven_button.png",
        "8": "eight_button.png",
        "9": "nine_button.png"
    }

    for _ in range(10):
        click_coordinates(*PHONE_KEYBOARD_COORDINATES["backspace_button"])

    for digit in PHONE_NUMBER:
        image_name = DIGITS[digit]
        click_coordinates(*PHONE_KEYBOARD_COORDINATES[image_name])
        time.sleep(0.2)

    time.sleep(1)
    for attempt in range(1, 4):
        phone_complete = (
            find_image("phone_field_filled.png", timeout=2) is not None
            or find_image("continue_button.png", timeout=2) is not None
        )
        if phone_complete:
            break

        print(
            f"[BENEFITS] Telefono incompleto; reintentando ultimo digito "
            f"({attempt}/3)"
        )
        click_coordinates(*PHONE_KEYBOARD_COORDINATES[DIGITS[PHONE_NUMBER[-1]]])
        time.sleep(1)
    else:
        raise ClickError("No se completo el numero de telefono Sevenly")

    save_screenshot("step_5_benefits_number_clicked")

    click_image("continue_button.png", timeout=10)

    time.sleep(4)

    save_screenshot("step_5.1_continue_benefits_number_clicked")

    # STEP 6 - WAIT FOR SEVENLY RESULT
    result_state = None
    started_at = time.monotonic()
    while time.monotonic() - started_at < 35:
        if find_image("dispatch_instructions_title.png", timeout=1) is not None:
            result_state = "dispatch"
            break

        if (
            find_image("start.png", timeout=1) is not None
            or find_image("iniciar.png", timeout=1) is not None
        ):
            result_state = "start"
            break

        if find_image("continue_button.png", timeout=1) is not None:
            click_image(
                "continue_button.png",
                timeout=3,
                use_coordinates=False,
                use_region=False,
            )
            time.sleep(4)
            continue

        time.sleep(1)

    if result_state is None:
        raise ClickError(
            "Sevenly no llego a despacho ni regreso a la pantalla INICIAR"
        )

    save_screenshot(f"step_6_sevenly_result_{result_state}")

    close_kiosk_after_checkpoint()
