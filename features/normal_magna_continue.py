from case_runner import run_stages
from clicker import assert_image_visible, click_coordinates, click_image
from features.applications import open_anydesk
from features.premium import handle_benefits_or_payment
from features.windows_app import run as windows_run
from screenshot import save_screenshot


FINALIZE_PURCHASE_SUMMARY_COORDINATES = (769, 524)


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def complete_payment_from_benefits():
    open_anydesk()

    handle_benefits_or_payment()

    click_asset("card.png", timeout=10)
    save_screenshot("normal_magna_continue_wait_payment")

    assert_image_visible("payment_success.png", confidence=0.80, timeout=30)
    save_screenshot("normal_magna_continue_payment_success")


def finalize_purchase_summary():
    open_anydesk()
    click_coordinates(*FINALIZE_PURCHASE_SUMMARY_COORDINATES)
    assert_image_visible("start.png", confidence=0.85, timeout=20)
    save_screenshot("normal_magna_continue_finalized_start_screen")


def run():
    return run_stages(
        [
            ("01_complete_payment_from_benefits", complete_payment_from_benefits),
            ("02_windows_app", windows_run),
            ("03_finalize_purchase_summary", finalize_purchase_summary),
        ]
    )
