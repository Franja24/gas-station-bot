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


def wait_for_image(image_name, confidence=0.45, timeout=10, region=None):
    print(f"[WAIT] Esperando {image_name} hasta {timeout}s")

    location = find_image(
        image_name,
        confidence=confidence,
        timeout=timeout,
        region=region
    )

    if location is None:
        print(f"[WAIT ERROR] No apareció {image_name}")
        return False

    print(f"[WAIT OK] {image_name} visible")
    return True
