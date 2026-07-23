import time

from case_runner import run_stages
from clicker import ClickError, assert_image_visible, click_image
from detector import find_image
from features.applications import open_anydesk
from features.sevenly_login import click_sevenly_account
from screenshot import save_screenshot


HUMAN_QR_WAIT_SECONDS = 3
ERROR_TIMEOUT_SECONDS = 45
ERROR_CLEAR_TIMEOUT_SECONDS = 12


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def _open_qr_scanner():
    print("[7LY QR] Abriendo inicio de sesión Sevenly")
    open_anydesk()
    click_sevenly_account()
    assert_image_visible("sevenly_qr_option.png", confidence=0.80, timeout=15)
    click_asset("sevenly_qr_option.png", timeout=10)
    assert_image_visible("sevenly_qr_waiting.png", confidence=0.80, timeout=15)
    save_screenshot("sevenly_qr_ready")


def _wait_until_previous_error_clears():
    started_at = time.monotonic()
    while time.monotonic() - started_at < ERROR_CLEAR_TIMEOUT_SECONDS:
        if find_image(
            "sevenly_error_toast.png",
            confidence=0.80,
            timeout=1,
        ) is None:
            return
        time.sleep(0.5)

    raise ClickError("El error Sevenly anterior no desapareció antes del segundo QR.")


def _restart_qr_scanner():
    print("[7LY QR] Reutilizando la pantalla para el segundo QR")
    open_anydesk()
    assert_image_visible("sevenly_qr_waiting.png", confidence=0.80, timeout=15)
    _wait_until_previous_error_clears()
    click_asset("sevenly_qr_scanner.png", timeout=10)
    save_screenshot("sevenly_qr_restarted")


def _wait_for_human_qr(person_name):
    print(
        f"[BOT_HUMANO] Presenta ahora el QR de {person_name}. "
        f"Espera inicial: {HUMAN_QR_WAIT_SECONDS} segundos."
    )
    time.sleep(HUMAN_QR_WAIT_SECONDS)


def _validate_error(person_name):
    assert_image_visible(
        "sevenly_error_toast.png",
        confidence=0.80,
        timeout=ERROR_TIMEOUT_SECONDS,
    )
    save_screenshot(f"sevenly_qr_{person_name.lower()}_error")
    print(f"[7LY QR] Error esperado confirmado para {person_name}")


def run(person_name, first_case=False):
    person_slug = person_name.strip().lower()
    prepare = _open_qr_scanner if first_case else _restart_qr_scanner

    return run_stages(
        [
            (f"00_prepare_qr_{person_slug}", prepare),
            (
                f"01_wait_human_qr_{person_slug}",
                lambda: _wait_for_human_qr(person_name),
            ),
            (
                f"02_validate_qr_error_{person_slug}",
                lambda: _validate_error(person_name),
            ),
        ]
    )
