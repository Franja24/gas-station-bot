from detector import find_image
from clicker import assert_image_visible, click_image
from features.kiosk_process import force_close_kiosk_process
from features.login import run as login_run
from features.manual_cancel_last_transation import (
    run as manual_cancel_last_transation_run,
)
from features.open_kiosco import run as open_kiosco_run
from features.out_of_service import is_out_of_service_visible
from screenshot import save_screenshot


def continue_active_session_if_visible(timeout=3):
    if find_image("continue_session_button.png", timeout=timeout) is None:
        return False

    click_image(
        "continue_session_button.png",
        timeout=10,
        use_coordinates=False,
        use_region=False,
    )

    if start_from_welcome_if_visible(timeout=5):
        return True

    assert_image_visible("premium.png", confidence=0.80, timeout=10)
    assert_image_visible("magna.png", confidence=0.80, timeout=10)

    save_screenshot("continue_session_clicked")

    return True


def start_from_welcome_if_visible(timeout=3):
    if find_image("iniciar.png", confidence=0.85, timeout=timeout) is None:
        return False

    click_image(
        "iniciar.png",
        confidence=0.85,
        timeout=5,
        use_coordinates=False,
        use_region=False,
    )

    assert_image_visible("premium.png", confidence=0.80, timeout=10)
    assert_image_visible("magna.png", confidence=0.80, timeout=10)

    save_screenshot("start_clicked_product_selection_visible")

    return True


def run():
    if find_image("premium.png", timeout=3) is not None:
        print("[LOGIN] Premium visible; sesión ya activa, saltando login.")
        save_screenshot("premium_visible_skip_login")
        return

    if start_from_welcome_if_visible(timeout=3):
        print("[LOGIN] Pantalla de inicio continuada.")
        return

    if continue_active_session_if_visible(timeout=3):
        print("[LOGIN] Sesión activa continuada.")
        return

    try:
        login_run()
    except Exception:
        if not is_out_of_service_visible(timeout=3):
            raise

        print(
            "[LOGIN] Bomba fuera de servicio; cancelando ultima transaccion."
        )

        save_screenshot("pump_out_of_service_detected")

        manual_cancel_last_transation_run()

        force_close_kiosk_process()

        open_kiosco_run()

        login_run()
