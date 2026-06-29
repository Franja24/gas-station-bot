from clicker import ClickError
from detector import find_image
from features.applications import open_anydesk
from features.out_of_service import is_out_of_service_visible
from screenshot import save_screenshot


def run():
    open_anydesk()

    if is_out_of_service_visible(timeout=5):
        save_screenshot("out_of_service_visible")
        return

    premium_visible = find_image("premium.png", confidence=0.80, timeout=5)
    magna_visible = find_image("magna.png", confidence=0.80, timeout=2)

    if premium_visible is not None and magna_visible is not None:
        save_screenshot("product_selection_visible")
        return

    raise ClickError(
        "No apareció Bomba Fuera de Servicio ni la pantalla Premium/Magna."
    )
