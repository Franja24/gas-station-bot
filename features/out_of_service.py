from detector import find_image


def is_out_of_service_visible(timeout=3):
    if find_image("pump_out_of_service_title.png", timeout=timeout) is None:
        return False

    return find_image("pump_out_of_service_icon.png", timeout=1) is not None
