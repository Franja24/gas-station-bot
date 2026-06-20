import time
from pathlib import Path

import pyautogui

from config.settings import (
    DETECTION_CONFIRMATIONS,
    DETECTION_LOCATION_TOLERANCE,
    DETECTION_POLL_INTERVAL,
    MIN_IMAGE_CONFIDENCE,
)
from screen_capture import get_target_monitor, locate_center_on_monitor


ASSETS_FOLDER = Path(__file__).resolve().parent / "assets"


def _same_location(first, second):
    return (
        abs(first.x - second.x) <= DETECTION_LOCATION_TOLERANCE
        and abs(first.y - second.y) <= DETECTION_LOCATION_TOLERANCE
    )


def find_image(
    image_name,
    confidence=MIN_IMAGE_CONFIDENCE,
    timeout=10,
    region=None,
):
    image_path = ASSETS_FOLDER / image_name

    if not image_path.is_file():
        raise FileNotFoundError(f"No existe la imagen: {image_path}")

    effective_confidence = max(confidence, MIN_IMAGE_CONFIDENCE)

    if confidence < MIN_IMAGE_CONFIDENCE:
        print(
            f"[WARN] Confianza {confidence:.2f} rechazada para {image_name}; "
            f"se usará el mínimo seguro {effective_confidence:.2f}"
        )

    start_time = time.monotonic()
    previous_location = None
    confirmations = 0
    target_monitor = get_target_monitor()

    while time.monotonic() - start_time < timeout:

        try:
            if target_monitor is None:
                location = pyautogui.locateCenterOnScreen(
                    str(image_path),
                    confidence=effective_confidence,
                    region=region,
                )
            else:
                location = locate_center_on_monitor(
                    image_path,
                    effective_confidence,
                    target_monitor,
                    region=region,
                )

            if location is not None:
                if (
                    previous_location is not None
                    and _same_location(previous_location, location)
                ):
                    confirmations += 1
                else:
                    confirmations = 1

                previous_location = location

                if confirmations >= DETECTION_CONFIRMATIONS:
                    print(
                        f"[OK] {image_name} confirmado {confirmations} veces "
                        f"en x={int(location.x)}, y={int(location.y)}"
                    )
                    return location
            else:
                previous_location = None
                confirmations = 0

        except pyautogui.ImageNotFoundException:
            previous_location = None
            confirmations = 0

        time.sleep(DETECTION_POLL_INTERVAL)

    return None
