import time
from pathlib import Path

import pyautogui

from config.asset_aliases import get_image_candidates
from config.settings import (
    DETECTION_CONFIRMATIONS,
    DETECTION_LOCATION_TOLERANCE,
    DETECTION_POLL_INTERVAL,
    MIN_IMAGE_CONFIDENCE,
)


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
    confirmations=DETECTION_CONFIRMATIONS,
):
    effective_confidence = max(confidence, MIN_IMAGE_CONFIDENCE)

    if confidence < MIN_IMAGE_CONFIDENCE:
        print(
            f"[WARN] Confianza {confidence:.2f} rechazada para {image_name}; "
            f"se usará el mínimo seguro {effective_confidence:.2f}"
        )

    candidates = get_image_candidates(image_name)

    required_confirmations = max(1, int(confirmations))

    for candidate_name in candidates:
        image_path = ASSETS_FOLDER / candidate_name

        if not image_path.is_file():
            continue

        start_time = time.monotonic()
        previous_location = None
        confirmations = 0

        while time.monotonic() - start_time < timeout:

            try:
                location = pyautogui.locateCenterOnScreen(
                    str(image_path),
                    confidence=effective_confidence,
                    region=region
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

                    if confirmations >= required_confirmations:
                        print(
                            f"[OK] {candidate_name} confirmado {confirmations} "
                            f"veces en x={int(location.x)}, y={int(location.y)}"
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
