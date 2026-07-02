from case_runner import run_stages
from clicker import assert_image_visible, click_coordinates
from detector import find_image
from features.applications import open_anydesk
from features.transaction_cancel_recovery import (
    FIRST_TRANSACTION_ROW_OFFSET,
    click_asset,
    click_relative_to_asset,
    open_transaction_register,
)
from screenshot import save_screenshot


EMPLOYEE_MENU_BUTTON_COORDINATES = (12, 67)
DECLINED_MESSAGE_METADATA_OFFSET = (428, 376)


def metadata_is_visible(timeout=1):
    return (
        find_image("metadata_title.png", confidence=0.80, timeout=timeout) is not None
        and find_image(
            "metadata_request_header.png",
            confidence=0.80,
            timeout=timeout,
        )
        is not None
        and find_image(
            "metadata_response_header.png",
            confidence=0.80,
            timeout=timeout,
        )
        is not None
    )


def stop_if_metadata_visible(stage_name):
    if metadata_is_visible(timeout=1):
        print(f"[DECLINED REQUEST] Metadata ya visible en {stage_name}")
        save_screenshot("00_declined_transaction_request_already_visible")
        return True

    return False


def return_to_product_selection():
    open_anydesk()

    if stop_if_metadata_visible("return_to_product_selection"):
        return

    click_asset("regresar_button.png", timeout=10)

    assert_image_visible("premium.png", confidence=0.80, timeout=15)
    assert_image_visible("magna.png", confidence=0.80, timeout=15)

    save_screenshot("01_product_selection_after_declined_payment")


def open_employee_menu():
    if stop_if_metadata_visible("open_employee_menu"):
        return

    click_coordinates(*EMPLOYEE_MENU_BUTTON_COORDINATES)

    assert_image_visible("employee_active_anchor.png", confidence=0.80, timeout=15)

    save_screenshot("02_employee_menu_visible")


def open_latest_transaction_summary():
    if stop_if_metadata_visible("open_latest_transaction_summary"):
        return

    open_transaction_register()

    click_relative_to_asset(
        "transaction_register_title.png",
        *FIRST_TRANSACTION_ROW_OFFSET,
    )

    assert_image_visible(
        "transaction_summary_title.png",
        confidence=0.80,
        timeout=15,
    )

    save_screenshot("04_declined_transaction_summary_visible")


def open_declined_request_metadata():
    if stop_if_metadata_visible("open_declined_request_metadata"):
        return

    click_relative_to_asset(
        "transaction_summary_title.png",
        *DECLINED_MESSAGE_METADATA_OFFSET,
    )

    assert_image_visible("metadata_title.png", confidence=0.80, timeout=10)
    assert_image_visible("metadata_request_header.png", confidence=0.80, timeout=10)
    assert_image_visible("metadata_response_header.png", confidence=0.80, timeout=10)

    save_screenshot("05_declined_transaction_request_visible")


def run():
    return run_stages(
        [
            ("01_return_to_product_selection", return_to_product_selection),
            ("02_open_employee_menu", open_employee_menu),
            ("03_open_latest_transaction_summary", open_latest_transaction_summary),
            ("04_open_declined_request_metadata", open_declined_request_metadata),
        ]
    )
