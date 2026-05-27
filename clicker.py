import pyautogui
from detector import find_image


def click_image(image_name, confidence=0.85, timeout=10):

    location = find_image(
        image_name,
        confidence=confidence,
        timeout=timeout
    )

    if location is None:
        print(f"[ERROR] No se encontró: {image_name}")
        return False

    pyautogui.moveTo(location.x, location.y, duration=0.3)
    pyautogui.click()

    print(f"[OK] Click en: {image_name}")

    return True