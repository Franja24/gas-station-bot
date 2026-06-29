import time

from clicker import assert_image_visible
from features.applications import open_anydesk
from features.kiosk_process import force_close_kiosk_process
from features.manual_cancel_last_transation import click_asset, open_settings_menu
from screenshot import save_screenshot


def click_back(step_name):
    click_asset("regresar_button.png", timeout=10)

    time.sleep(1)

    save_screenshot(step_name)


def run(force_close_after=True):
    print("Cancelando transaccion y continuando sesion")

    open_anydesk()

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

    click_asset("transaction_log_first_row_marker.png", timeout=10)

    assert_image_visible(
        "transaction_summary_title.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("step_4_latest_transaction_visible")

    click_asset("cancel_transaction_button.png", timeout=10)

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

    click_back("step_7_back_to_transaction_log")

    assert_image_visible(
        "transaction_log_title.png",
        confidence=0.80,
        timeout=10,
    )

    click_back("step_8_back_to_settings")

    assert_image_visible(
        "continue_session_button.png",
        confidence=0.80,
        timeout=10,
    )

    click_asset("continue_session_button.png", timeout=10)

    assert_image_visible("premium.png", confidence=0.80, timeout=10)
    assert_image_visible("magna.png", confidence=0.80, timeout=10)

    save_screenshot("step_9_product_selection_visible")

    if not force_close_after:
        return

    force_close_kiosk_process()

    save_screenshot("step_10_kiosk_process_force_close")
