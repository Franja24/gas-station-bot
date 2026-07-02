import time

from case_runner import run_stages
from clicker import ClickError, assert_image_visible, click_coordinates, click_image
from config.settings import SCREENSHOT_TO_MOUSE_SCALE
from detector import find_image
from features.applications import open_anydesk
from features.login import run as login_run
from features.magna import run as magna_run
from features.open_kiosco import run as open_kiosco_run
from features.windows_app import run as windows_run
import pyautogui
from screenshot import save_screenshot


FINALIZE_BUTTON_REGION = (900, 700, 900, 500)


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def click_calibrated(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=True,
        use_region=False,
    )


def is_visible(image_name, timeout=2):
    return find_image(image_name, confidence=0.80, timeout=timeout) is not None


def product_selection_visible(timeout=2):
    if not is_visible("premium.png", timeout=timeout):
        return False

    assert_image_visible("magna.png", confidence=0.80, timeout=10)
    return True


def purchase_summary_visible(timeout=2):
    if is_visible("purchase_summary_title.png", timeout=timeout):
        return True

    return (
        find_image(
            "finalize_button.png",
            confidence=0.80,
            timeout=timeout,
            region=FINALIZE_BUTTON_REGION,
        )
        is not None
    )


def click_start_button():
    started_at = time.monotonic()
    attempts = 0
    static_points = [
        (700, 520),
        (640, 496),
        (598, 367),
        (640, 456),
    ]

    while time.monotonic() - started_at < 35:
        if product_selection_visible(timeout=1):
            save_screenshot("normal_magna_start_already_on_product_selection")
            return

        start_location = find_image("start.png", confidence=0.80, timeout=2)
        if start_location is None:
            start_location = find_image("iniciar.png", confidence=0.80, timeout=1)

        dynamic_points = []
        if start_location is not None:
            start_x = int(start_location.x * SCREENSHOT_TO_MOUSE_SCALE)
            start_y = int(start_location.y * SCREENSHOT_TO_MOUSE_SCALE)
            dynamic_points = [
                (start_x, start_y),
                (start_x, start_y + 18),
                (start_x + 70, start_y),
                (start_x - 70, start_y),
                (start_x, start_y - 18),
            ]

        seen_points = set()
        for point in dynamic_points + static_points:
            if point in seen_points:
                continue
            seen_points.add(point)

            attempts += 1
            print(f"[START] Intento {attempts}: clic en INICIAR x={point[0]}, y={point[1]}")
            click_coordinates(*point)
            time.sleep(1.5)

            if product_selection_visible(timeout=2):
                save_screenshot("normal_magna_start_clicked")
                return

        pyautogui.press("esc")
        time.sleep(1)
        open_anydesk()

    raise ClickError("No se pudo avanzar desde INICIAR a selección de producto.")


def ensure_product_selection_from_start():
    click_start_button()
    assert_image_visible("premium.png", confidence=0.80, timeout=15)
    assert_image_visible("magna.png", confidence=0.80, timeout=10)


def wait_for_start_or_product_selection(timeout=30):
    started_at = time.monotonic()

    while time.monotonic() - started_at < timeout:
        if purchase_summary_visible(timeout=1):
            continue

        if product_selection_visible(timeout=1):
            save_screenshot("normal_magna_finalized_product_selection")
            return

        if is_visible("start.png", timeout=1) or is_visible("iniciar.png", timeout=1):
            save_screenshot("normal_magna_finalized_start_screen")
            return

    raise ClickError("No apareció pantalla final de inicio ni selección.")


def click_finalize_button():
    try:
        click_image(
            "finalize_button.png",
            timeout=5,
            use_coordinates=False,
            use_region=False,
            region=FINALIZE_BUTTON_REGION,
        )
    except ClickError as exc:
        print(
            f"[FALLBACK] finalize_button.png no se pudo usar por asset: {exc}. "
            "Intentando coordenada calibrada."
        )
        click_coordinates(770, 520)


def finalize_visible_purchase_summary():
    for attempt in range(1, 4):
        assert_image_visible("purchase_summary_title.png", confidence=0.80, timeout=30)
        print(f"[FINALIZE] Intento {attempt}: clic en Finalizar")
        click_finalize_button()
        time.sleep(2)

        if not purchase_summary_visible(timeout=2):
            wait_for_start_or_product_selection(timeout=30)
            return

    save_screenshot("normal_magna_finalize_still_on_purchase_summary")
    raise ClickError("No se pudo salir de Resumen de Compra con Finalizar.")


def prepare_product_selection():
    open_anydesk()
    pyautogui.press("esc")

    if purchase_summary_visible():
        finalize_visible_purchase_summary()
        if is_visible("start.png", timeout=20) or is_visible("iniciar.png"):
            ensure_product_selection_from_start()
        else:
            assert_image_visible("premium.png", confidence=0.80, timeout=20)
            assert_image_visible("magna.png", confidence=0.80, timeout=10)
        save_screenshot("normal_magna_purchase_summary_finalized")
        return

    if is_visible("amount_1250.png", timeout=5):
        save_screenshot("normal_magna_amount_selection_ready")
        return

    if is_visible("magna.png") or is_visible("premium.png"):
        save_screenshot("normal_magna_product_selection_ready")
        return

    if is_visible("start.png") or is_visible("iniciar.png"):
        ensure_product_selection_from_start()
        save_screenshot("normal_magna_start_clicked")
        return

    if is_visible("login_button.png"):
        login_run()
        return

    open_kiosco_run()

    if is_visible("amount_1250.png", timeout=5):
        save_screenshot("normal_magna_amount_selection_ready")
        return

    if is_visible("magna.png") or is_visible("premium.png"):
        save_screenshot("normal_magna_product_selection_ready")
        return

    if is_visible("start.png") or is_visible("iniciar.png"):
        ensure_product_selection_from_start()
        save_screenshot("normal_magna_start_clicked")
        return

    if is_visible("login_button.png"):
        login_run()
        return

    raise ClickError("No se pudo preparar kiosco para selección de producto.")


def finalize_purchase_summary():
    open_anydesk()
    finalize_visible_purchase_summary()


def run():
    return run_stages(
        [
            ("00_prepare_product_selection", prepare_product_selection),
            ("01_magna", magna_run),
            ("02_windows_app", windows_run),
            ("03_finalize_purchase_summary", finalize_purchase_summary),
        ]
    )
