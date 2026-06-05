import pyautogui
import time


def find_image(image_name, confidence=0.45, timeout=10, region=None):

    start_time = time.time()

    while time.time() - start_time < timeout:

        try:
            location = pyautogui.locateCenterOnScreen(
                f"assets/{image_name}",
                confidence=confidence,
                region=region
            )

            if location is not None:
                return location

        except pyautogui.ImageNotFoundException:
            pass

        time.sleep(0.5)

    return None