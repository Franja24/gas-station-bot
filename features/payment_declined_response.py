from clicker import assert_image_visible, click_image
from detector import find_image
from features.applications import open_anydesk
from features.manual_cancel_last_transation import click_asset, open_settings_menu
from screenshot import save_screenshot


DECLINED_RESPONSE_TABLE_REGION = (1300, 450, 500, 180)


def click_declined_response_eye():
    return click_image(
        "declined_response_eye_button.png",
        timeout=10,
        use_coordinates=False,
        use_region=False,
        region=DECLINED_RESPONSE_TABLE_REGION,
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
        region=DECLINED_RESPONSE_TABLE_REGION,
    )

    save_screenshot("declined_step_5_latest_declined_transaction_visible")

    click_declined_response_eye()

    assert_image_visible("metadata_response_title.png", confidence=0.80, timeout=10)

    save_screenshot("declined_step_6_response_metadata_visible")


def return_to_product_selection_after_log_review():
    click_asset("metadata_close_button.png", timeout=10)

    for step in range(1, 4):
        click_asset("regresar_button.png", timeout=10)
        save_screenshot(f"declined_step_7_back_{step}")

    if find_image("continue_session_button.png", timeout=3) is not None:
        click_asset("continue_session_button.png", timeout=10)

    assert_image_visible("premium.png", confidence=0.80, timeout=15)
    assert_image_visible("magna.png", confidence=0.80, timeout=15)
    save_screenshot("declined_step_8_product_selection_restored")


def run(open_app=True):
    print("Validando response de pago declinado")

    if open_app:
        open_anydesk()

    return_to_product_selection_from_decline()
    open_transaction_log_from_settings()
    open_latest_declined_response()
    return_to_product_selection_after_log_review()
