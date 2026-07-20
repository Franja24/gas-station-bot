import time

from clicker import assert_image_visible
from features.applications import open_anydesk
from features.manual_cancel_last_transation import click_asset, open_settings_menu
from features.transaction_log_selection import click_transaction
from screenshot import save_screenshot


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

    click_asset("confirm_transaction_button.png", timeout=10)

    assert_image_visible(
        "confirm_transaction_modal_button.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("step_4_confirm_transaction_clicked")

    click_asset("confirm_transaction_modal_button.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_5_transaction_confirmed")

    assert_image_visible("finalize_button.png", confidence=0.80, timeout=10)

    click_asset("finalize_button.png", timeout=10)

    time.sleep(2)

    save_screenshot("step_6_finalize_clicked")
