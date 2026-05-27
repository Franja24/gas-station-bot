import pyautogui
import time


def find_image(image_name, confidence=0.85, timeout=10):
    start_time = time.time()

    while time.time() - start_time < timeout:

        location = pyautogui.locateCenterOnScreen(
            f"assets/{image_name}",
            confidence=confidence
        )

        if location is not None:
            return location

        time.sleep(0.5)

    return None