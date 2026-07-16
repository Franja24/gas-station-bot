from config.local_coordinates import load_local_settings


_LOCAL_SETTINGS = load_local_settings(
    {
        "reference_screen_size": (1280, 800),
        "screenshot_to_mouse_scale": 0.5,
    }
)


REFERENCE_SCREEN_SIZE = _LOCAL_SETTINGS["reference_screen_size"]

# Las capturas de macOS Retina usan el doble de pixeles que las coordenadas
# logicas empleadas por el mouse.
SCREENSHOT_TO_MOUSE_SCALE = _LOCAL_SETTINGS["screenshot_to_mouse_scale"]

MIN_IMAGE_CONFIDENCE = 0.80
DETECTION_CONFIRMATIONS = 2
DETECTION_LOCATION_TOLERANCE = 8
DETECTION_POLL_INTERVAL = 0.35

CLICK_MOVE_DURATION = 0.5
CLICK_HOLD_SECONDS = 0.15
