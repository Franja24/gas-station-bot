from config.local_coordinates import load_local_coordinates


DEFAULT_PHONE_KEYBOARD_COORDINATES = {
    "one_button.png": (520, 260),
    "two_button.png": (650, 260),
    "three_button.png": (780, 260),
    "four_button.png": (520, 340),
    "five_button.png": (650, 340),
    "six_button.png": (780, 340),
    "seven_button.png": (520, 400),
    "eight_button.png": (650, 400),
    "nine_button.png": (780, 400),
    "zero_button.png": (650, 460),
}


PHONE_KEYBOARD_COORDINATES = load_local_coordinates(
    "phone_keyboard",
    DEFAULT_PHONE_KEYBOARD_COORDINATES,
)
