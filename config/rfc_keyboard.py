from config.local_coordinates import load_local_coordinates


DEFAULT_RFC_KEYBOARD_COORDINATES = {
    "rfc_one.png": (490, 260),
    "rfc_zero.png": (780, 260),
    "rfc_a.png": (490, 380),
    "rfc_x.png": (560, 420),
}


RFC_KEYBOARD_COORDINATES = load_local_coordinates(
    "rfc_keyboard",
    DEFAULT_RFC_KEYBOARD_COORDINATES,
)
