from detector import find_image
from features.login import run as login_run
from features.out_of_service import is_out_of_service_visible
from screenshot import save_screenshot


def run():
    if find_image("premium.png", timeout=2) is not None:
        save_screenshot("premium_visible_skip_login_for_confirm")
        return

    if is_out_of_service_visible(timeout=2):
        save_screenshot("out_of_service_skip_login_for_confirm")
        return

    login_run()
