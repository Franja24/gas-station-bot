import time

from clicker import ClickError, click_image
from detector import find_image
from features.applications import open_anydesk
from screenshot import save_screenshot


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def wait_for_login_or_selection(timeout=15):
    start_time = time.monotonic()

    while time.monotonic() - start_time < timeout:
        if find_image("login_button.png", timeout=1) is not None:
            return "login"

        if find_image("premium.png", timeout=1) is not None:
            return "selection"

    raise ClickError(
        "No apareció login_button.png ni premium.png después de INICIAR."
    )


def run():
    print("Iniciando sesión del kiosko desde pantalla INICIAR")

    open_anydesk()

    if find_image("premium.png", timeout=2) is not None:
        print("[START] Premium visible; pantalla de selección ya está lista.")
        save_screenshot("step_0_selection_already_visible")
        return

    if find_image("login_button.png", timeout=2) is not None:
        print("[START] Login visible; listo para capturar credenciales.")
        save_screenshot("step_0_login_already_visible")
        return

    click_asset("iniciar.png", timeout=10)

    save_screenshot("step_1_iniciar_clicked")

    next_state = wait_for_login_or_selection()

    save_screenshot(f"step_2_{next_state}_visible")
