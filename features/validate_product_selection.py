from clicker import assert_image_visible
from features.applications import open_anydesk
from screenshot import save_screenshot


def run():
    open_anydesk()

    assert_image_visible("premium.png", confidence=0.80, timeout=10)
    assert_image_visible("magna.png", confidence=0.80, timeout=10)

    save_screenshot("product_selection_premium_magna_visible")
