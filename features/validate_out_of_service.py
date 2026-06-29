from clicker import assert_image_visible
from features.applications import open_anydesk
from screenshot import save_screenshot


def run():
    open_anydesk()

    assert_image_visible(
        "pump_out_of_service_title.png",
        confidence=0.80,
        timeout=10,
    )
    assert_image_visible(
        "pump_out_of_service_icon.png",
        confidence=0.80,
        timeout=10,
    )

    save_screenshot("out_of_service_visible")
