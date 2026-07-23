import time

from clicker import ClickError, assert_image_visible, click_image
from detector import find_image
from features.applications import open_anydesk
from features.manual_cancel_last_transation import click_asset, open_settings_menu
from features.platform_profile import use_windows_path
from screenshot import save_screenshot


DECLINED_RESPONSE_TABLE_REGION = (1300, 450, 500, 180)
DECLINED_RESPONSE_TABLE_REGION_WINDOWS = (1050, 300, 200, 150)


def declined_response_table_region():
    if use_windows_path():
        return DECLINED_RESPONSE_TABLE_REGION_WINDOWS

    return DECLINED_RESPONSE_TABLE_REGION


def click_declined_response_eye():
    return click_image(
        "declined_response_eye_button.png",
        timeout=10,
        use_coordinates=False,
        use_region=False,
        region=declined_response_table_region(),
    )


def return_to_product_selection_from_decline():
    assert_image_visible("payment_declined_title.png", confidence=0.80, timeout=10)

    save_screenshot("declined_step_1_payment_declined_visible")

    click_asset("regresar_button.png", timeout=10)

    assert_image_visible("premium.png", confidence=0.80, timeout=10)
    assert_image_visible("magna.png", confidence=0.80, timeout=10)

    save_screenshot("declined_step_2_product_selection_visible")


def open_transaction_log_from_settings():
    open_settings_menu()

    assert_image_visible(
        "settings_transaction_log_option.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("declined_step_3_settings_visible")

    click_asset("settings_transaction_log_option.png", timeout=10)

    assert_image_visible(
        "transaction_log_title.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("declined_step_4_transaction_log_visible")


def open_latest_declined_response():
    click_asset("transaction_log_first_row_marker.png", timeout=10)

    assert_image_visible(
        "transaction_summary_title.png",
        confidence=0.80,
        timeout=10,
    )
    assert_image_visible(
        "declined_response_eye_button.png",
        confidence=0.80,
        timeout=10,
        region=declined_response_table_region(),
    )

    save_screenshot("declined_step_5_latest_declined_transaction_visible")

    click_declined_response_eye()

    assert_image_visible("metadata_response_title.png", confidence=0.80, timeout=10)

    save_screenshot("declined_step_6_response_metadata_visible")


def wait_for_restored_kiosk_state(timeout=20):
    started_at = time.monotonic()

    while time.monotonic() - started_at < timeout:
        if (
            find_image("premium.png", timeout=1) is not None
            and find_image("magna.png", timeout=1) is not None
        ):
            return "product_selection"

        if find_image("start.png", timeout=1) is not None:
            return "start"

        if find_image("iniciar.png", timeout=1) is not None:
            return "start"

    raise ClickError(
        "No apareció selección de combustible ni pantalla Iniciar "
        "después de consultar el log declinado."
    )


def return_to_product_selection_after_log_review():
    click_asset("metadata_close_button.png", timeout=10)

    for step in range(1, 4):
        click_asset("regresar_button.png", timeout=10)
        save_screenshot(f"declined_step_7_back_{step}")

    if find_image("continue_session_button.png", timeout=3) is not None:
        click_asset("continue_session_button.png", timeout=10)

    restored_state = wait_for_restored_kiosk_state()
    save_screenshot(f"declined_step_8_{restored_state}_restored")
    return restored_state


def run(open_app=True):
    print("Validando response de pago declinado")

    if open_app:
        open_anydesk()

    return_to_product_selection_from_decline()
    open_transaction_log_from_settings()
    open_latest_declined_response()
    return_to_product_selection_after_log_review()
