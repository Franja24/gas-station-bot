from detector import find_image
from features.login import run as login_run
from features.manual_cancel_last_transation import (
    run as manual_cancel_last_transation_run,
)
from features.out_of_service import is_out_of_service_visible
from screenshot import save_screenshot


def run():
    if find_image("premium.png", timeout=3) is not None:
        print("[LOGIN] Premium visible; sesión ya activa, saltando login.")
        save_screenshot("premium_visible_skip_login")
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

        login_run()
