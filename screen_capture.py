import os
from types import SimpleNamespace

SCREEN_INDEX_ENV = "GAS_STATION_SCREEN_INDEX"


def get_target_screen_index():
    raw_value = os.getenv(SCREEN_INDEX_ENV)

    if not raw_value:
        return None

    try:
        screen_index = int(raw_value)
    except ValueError as error:
        raise ValueError(
            f"{SCREEN_INDEX_ENV} debe ser un número de pantalla, por ejemplo 2."
        ) from error

    if screen_index < 1:
        raise ValueError(f"{SCREEN_INDEX_ENV} debe ser 1 o mayor.")

    return screen_index


def get_monitors():
    from mss import MSS

    with MSS() as screenshot_tool:
        return [dict(monitor) for monitor in screenshot_tool.monitors]


def get_virtual_screen_bounds():
    return get_monitors()[0]


def get_target_monitor():
    screen_index = get_target_screen_index()

    if screen_index is None:
        return None

    monitors = get_monitors()

    if screen_index >= len(monitors):
        available = len(monitors) - 1
        raise ValueError(
            f"{SCREEN_INDEX_ENV}={screen_index} no existe. "
            f"Pantallas disponibles: 1-{available}."
        )

    return monitors[screen_index]


def get_target_screen_size():
    monitor = get_target_monitor()

    if monitor is None:
        return None

    return (monitor["width"], monitor["height"])


def to_target_screen_coordinates(x, y):
    monitor = get_target_monitor()

    if monitor is None:
        return (x, y)

    return (monitor["left"] + x, monitor["top"] + y)


def from_target_screen_coordinates(x, y):
    monitor = get_target_monitor()

    if monitor is None:
        return (x, y)

    return (x - monitor["left"], y - monitor["top"])


def _region_bounds(monitor, region):
    if region is None:
        return dict(monitor)

    x, y, width, height = region

    return {
        "left": monitor["left"] + x,
        "top": monitor["top"] + y,
        "width": width,
        "height": height,
    }


def capture_screen(bounds):
    from mss import MSS
    from PIL import Image

    with MSS() as screenshot_tool:
        screenshot = screenshot_tool.grab(bounds)

    return Image.frombytes("RGB", screenshot.size, screenshot.rgb)


def capture_target_screen():
    monitor = get_target_monitor()

    if monitor is None:
        return None

    return capture_screen(monitor)


def locate_center_on_monitor(image_path, confidence, monitor, region=None):
    import pyscreeze

    bounds = _region_bounds(monitor, region)
    screenshot = capture_screen(bounds)

    try:
        try:
            location = pyscreeze.locate(
                str(image_path),
                screenshot,
                confidence=confidence,
            )
        except NotImplementedError:
            location = pyscreeze.locate(str(image_path), screenshot)
    except pyscreeze.ImageNotFoundException:
        return None

    if location is None:
        return None

    return SimpleNamespace(
        x=bounds["left"] + location.left + location.width / 2,
        y=bounds["top"] + location.top + location.height / 2,
    )
