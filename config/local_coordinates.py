import json
from pathlib import Path


LOCAL_COORDINATES_PATH = Path(__file__).with_name("coordinates.local.json")


class CoordinateConfigError(ValueError):
    pass


def _load_local_config(path=LOCAL_COORDINATES_PATH):
    if not path.is_file():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CoordinateConfigError(
            f"JSON invalido en {path}: {exc.msg}"
        ) from exc

    if not isinstance(data, dict):
        raise CoordinateConfigError(
            f"{path} debe contener un objeto JSON en la raiz."
        )

    return data


def _normalize_coordinate(section_name, key, value):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise CoordinateConfigError(
            f"{section_name}.{key} debe ser una lista [x, y]."
        )

    x, y = value

    if not isinstance(x, int) or not isinstance(y, int):
        raise CoordinateConfigError(
            f"{section_name}.{key} debe usar enteros: [x, y]."
        )

    return (x, y)


def load_local_coordinates(section_name, default_coordinates, path=None):
    local_config = _load_local_config(path or LOCAL_COORDINATES_PATH)
    overrides = local_config.get(section_name, {})

    if not isinstance(overrides, dict):
        raise CoordinateConfigError(
            f"La seccion {section_name} debe contener un objeto JSON."
        )

    coordinates = dict(default_coordinates)

    for key, value in overrides.items():
        coordinates[key] = _normalize_coordinate(section_name, key, value)

    return coordinates


def load_local_settings(default_settings, path=None):
    local_config = _load_local_config(path or LOCAL_COORDINATES_PATH)
    overrides = local_config.get("settings", {})

    if not isinstance(overrides, dict):
        raise CoordinateConfigError(
            "La seccion settings debe contener un objeto JSON."
        )

    settings = dict(default_settings)

    if "reference_screen_size" in overrides:
        settings["reference_screen_size"] = _normalize_coordinate(
            "settings",
            "reference_screen_size",
            overrides["reference_screen_size"],
        )

    if "screenshot_to_mouse_scale" in overrides:
        scale = overrides["screenshot_to_mouse_scale"]

        if not isinstance(scale, (int, float)):
            raise CoordinateConfigError(
                "settings.screenshot_to_mouse_scale debe ser un numero."
            )

        settings["screenshot_to_mouse_scale"] = float(scale)

    return settings
