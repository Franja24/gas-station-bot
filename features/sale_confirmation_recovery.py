from clicker import assert_image_visible
from features.transaction_cancel_recovery import (
    CONFIRM_CANCEL_OFFSET,
    CONTINUE_SESSION_OFFSET,
    FIRST_TRANSACTION_ROW_OFFSET,
    click_asset,
    click_relative_to_asset,
    login_to_employee_menu,
    open_transaction_register,
)
from screenshot import save_screenshot


def trigger_out_of_service():
    click_relative_to_asset("employee_active_anchor.png", *CONTINUE_SESSION_OFFSET)

    assert_image_visible(
        "pump_out_of_service_title.png",
        confidence=0.80,
        timeout=15,
    )

    save_screenshot("01_pump_out_of_service_visible")

    assert_image_visible(
        "employee_active_anchor.png",
        confidence=0.80,
        timeout=20,
    )

    save_screenshot("02_employee_menu_after_out_of_service")


def confirm_latest_transaction():
    click_relative_to_asset(
        "transaction_register_title.png",
        *FIRST_TRANSACTION_ROW_OFFSET,
    )

    assert_image_visible(
        "transaction_summary_title.png",
        confidence=0.80,
        timeout=15,
    )

    save_screenshot("03_transaction_summary_visible")

    click_asset("confirm_transaction_button.png", timeout=10)

    assert_image_visible(
        "confirm_transaction_modal_title.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("04_confirm_transaction_modal_visible")

    click_relative_to_asset(
        "confirm_transaction_modal_title.png",
        *CONFIRM_CANCEL_OFFSET,
    )

    assert_image_visible(
        "purchase_summary_title.png",
        confidence=0.80,
        timeout=20,
    )

    save_screenshot("05_purchase_summary_visible")


def finalize_sale():
    click_asset("finalize_button.png", timeout=10)

    assert_image_visible("premium.png", confidence=0.80, timeout=30)

    save_screenshot("06_start_screen_visible")


def run():
    login_to_employee_menu()
    trigger_out_of_service()
    open_transaction_register()
    confirm_latest_transaction()
    finalize_sale()
