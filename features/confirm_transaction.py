import time

from clicker import assert_image_visible, click_coordinates
from detector import find_image
from features.applications import open_anydesk
from features.manual_cancel_last_transation import click_asset, open_settings_menu
from features.transaction_log_selection import click_transaction
from screenshot import save_screenshot


CONFIRM_TRANSACTION_FALLBACK = (1165, 1085)
CONFIRM_MODAL_FALLBACK = (1140, 638)
FINALIZE_TRANSACTION_FALLBACK = (1135, 754)


def return_from_approved_transaction():
    print("[TRANSACTION] La operacion ya esta aprobada; regresando a la sesion")
    save_screenshot("step_4_transaction_already_approved")

    click_asset("regresar_button.png", timeout=10)
    assert_image_visible("transaction_log_title.png", confidence=0.80, timeout=10)
    save_screenshot("step_5_back_to_transaction_log")

    click_asset("regresar_button.png", timeout=10)
    assert_image_visible(
        "settings_transaction_log_option.png",
        confidence=0.80,
        timeout=10,
    )
    save_screenshot("step_6_back_to_settings")

    click_asset("regresar_button.png", timeout=10)
    assert_image_visible(
        "continue_session_button.png",
        confidence=0.80,
        timeout=10,
    )
    save_screenshot("step_7_back_to_employee_session")

    click_asset("continue_session_button.png", timeout=10)
    save_screenshot("step_8_approved_transaction_finished")

    return "already_approved"


def recover_open_transaction():
    confirm_button = find_image(
        "confirm_transaction_button.png",
        confidence=0.80,
        timeout=3,
    )

    if confirm_button is None:
        cancel_button = find_image(
            "cancel_transaction_button.png",
            confidence=0.80,
            timeout=3,
        )
        if cancel_button is not None:
            return return_from_approved_transaction()

        print(
            "[TRANSACTION] Asset de Confirmar no detectado; "
            "usando coordenada Windows calibrada"
        )
        click_coordinates(*CONFIRM_TRANSACTION_FALLBACK)
    else:
        click_asset("confirm_transaction_button.png", timeout=10)

    save_screenshot("step_4_confirm_transaction_clicked")

    modal_button = find_image(
        "confirm_transaction_modal_button.png",
        confidence=0.80,
        timeout=5,
    )
    if modal_button is None:
        print(
            "[TRANSACTION] Asset del modal no detectado; "
            "usando coordenada Windows calibrada"
        )
        click_coordinates(*CONFIRM_MODAL_FALLBACK)
    else:
        click_asset("confirm_transaction_modal_button.png", timeout=10)

    time.sleep(12)

    save_screenshot("step_5_transaction_confirmed")

    finalize_button = find_image(
        "finalize_button.png",
        confidence=0.80,
        timeout=10,
    )
    if finalize_button is None:
        print(
            "[TRANSACTION] Asset de Finalizar no detectado; "
            "usando coordenada Windows calibrada"
        )
        click_coordinates(*FINALIZE_TRANSACTION_FALLBACK)
    else:
        click_asset("finalize_button.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_6_finalize_clicked")

    return "confirmed"


def run(expected_amount=None):
    print("Confirmando manualmente la ultima transaccion")

    open_anydesk()

    open_settings_menu()

    assert_image_visible(
        "settings_transaction_log_option.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("step_1_settings_visible")

    click_asset("settings_transaction_log_option.png", timeout=10)

    assert_image_visible(
        "transaction_log_title.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("step_2_transaction_log_visible")

    click_transaction(expected_amount)

    assert_image_visible(
        "transaction_summary_title.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("step_3_latest_transaction_visible")

    return recover_open_transaction()
