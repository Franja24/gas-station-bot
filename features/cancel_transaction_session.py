import time

from clicker import assert_image_visible
from detector import find_image
from features.applications import open_anydesk
from features.kiosk_process import force_close_kiosk_process
from features.manual_cancel_last_transation import click_asset, open_settings_menu
from features.transaction_log_selection import click_transaction
from screenshot import save_screenshot


def click_back(step_name):
    click_asset("regresar_button.png", timeout=10)

    time.sleep(1)

    save_screenshot(step_name)


def resume_from_settings():
    assert_image_visible(
        "settings_transaction_log_option.png",
        confidence=0.80,
        timeout=10,
    )
    click_back("resume_back_to_session")
    assert_image_visible(
        "continue_session_button.png",
        confidence=0.80,
        timeout=10,
    )
    click_asset("continue_session_button.png", timeout=10)
    assert_image_visible(
        "pump_out_of_service_title.png",
        confidence=0.80,
        timeout=10,
    )
    save_screenshot("resume_pump_out_of_service_visible")


def run(force_close_after=True, expected_amount=None):
    print("Cancelando transaccion y continuando sesion")

    open_anydesk()

    transaction_summary_visible = find_image(
        "transaction_summary_title.png",
        confidence=0.80,
        timeout=2,
    )

    if transaction_summary_visible is None:
        assert_image_visible(
            "pump_out_of_service_title.png",
            confidence=0.80,
            timeout=10,
        )
        assert_image_visible(
            "pump_out_of_service_icon.png",
            confidence=0.80,
            timeout=10,
        )

        save_screenshot("step_1_pump_out_of_service_visible")

        open_settings_menu()

        assert_image_visible(
            "settings_transaction_log_option.png",
            confidence=0.80,
            timeout=10,
        )

        save_screenshot("step_2_settings_visible")

        click_asset("settings_transaction_log_option.png", timeout=10)

        assert_image_visible(
            "transaction_log_title.png",
            confidence=0.80,
            timeout=10,
        )

        save_screenshot("step_3_transaction_log_visible")

        click_transaction(expected_amount)

        assert_image_visible(
            "transaction_summary_title.png",
            confidence=0.80,
            timeout=10,
        )
    else:
        print("[CLEANUP] Reanudando desde el detalle de la última transacción.")

    save_screenshot("step_4_latest_transaction_visible")

    cancel_button = find_image(
        "cancel_transaction_button.png",
        confidence=0.80,
        timeout=3,
    )

    if cancel_button is not None:
        click_asset("cancel_transaction_button.png", timeout=3)

        assert_image_visible(
            "confirm_cancel_transaction_button.png",
            confidence=0.80,
            timeout=10,
        )

        time.sleep(3)

        save_screenshot("step_5_cancel_transaction_clicked")

        click_asset("confirm_cancel_transaction_button.png", timeout=10)

        time.sleep(2)

        save_screenshot("step_6_cancel_transaction_confirmed")
    else:
        assert_image_visible(
            "transaction_declined_message.png",
            confidence=0.80,
            timeout=5,
        )
        print(
            "[CLEANUP] La última transacción ya está declinada; "
            "no requiere cancelación."
        )
        save_screenshot("step_6_latest_transaction_already_declined")

    click_back("step_7_back_to_transaction_log")

    assert_image_visible(
        "transaction_log_title.png",
        confidence=0.80,
        timeout=10,
    )

    click_back("step_8_back_to_settings")

    assert_image_visible(
        "settings_transaction_log_option.png",
        confidence=0.80,
        timeout=10,
    )

    click_back("step_9_back_to_session")

    assert_image_visible(
        "continue_session_button.png",
        confidence=0.80,
        timeout=10,
    )

    click_asset("continue_session_button.png", timeout=10)

    if not force_close_after:
        assert_image_visible(
            "pump_out_of_service_title.png",
            confidence=0.80,
            timeout=10,
        )
        save_screenshot("step_10_pump_out_of_service_visible")
        return

    assert_image_visible("premium.png", confidence=0.80, timeout=10)
    assert_image_visible("magna.png", confidence=0.80, timeout=10)

    save_screenshot("step_10_product_selection_visible")

    force_close_kiosk_process()

    save_screenshot("step_11_kiosk_process_force_close")
