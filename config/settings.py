from config.local_coordinates import load_reference_screen_size


DEFAULT_REFERENCE_SCREEN_SIZE = (1280, 800)
REFERENCE_SCREEN_SIZE = load_reference_screen_size(DEFAULT_REFERENCE_SCREEN_SIZE)

# Las capturas de macOS Retina usan el doble de pixeles que las coordenadas
# logicas empleadas por el mouse.
SCREENSHOT_TO_MOUSE_SCALE = 0.5

MIN_IMAGE_CONFIDENCE = 0.80
DETECTION_CONFIRMATIONS = 2
DETECTION_LOCATION_TOLERANCE = 8
DETECTION_POLL_INTERVAL = 0.35

CLICK_MOVE_DURATION = 0.5
CLICK_HOLD_SECONDS = 0.15
