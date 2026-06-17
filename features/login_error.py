from features.applications import open_anydesk
from clicker import click_image_asset
from detector import wait_for_image
from screenshot import save_screenshot, generate_pdf_report


INVALID_USER = [
    "login_two_button.png",
]

INVALID_PASSWORD = [
    "login_one_button.png",
    "login_one_button.png",
    "login_one_button.png",
    "login_one_button.png",
    "login_one_button.png",
    "login_one_button.png",
]


def wait_asset(image_name, confidence, timeout):
    if not wait_for_image(image_name, confidence=confidence, timeout=timeout):
        raise RuntimeError(f"No apareció el asset requerido: {image_name}")


def click_asset(image_name, confidence, timeout):
    if not click_image_asset(
        image_name,
        confidence=confidence,
        timeout=timeout
    ):
        raise RuntimeError(f"No se pudo hacer click por asset: {image_name}")


def click_digits(digits, confidence=0.25, timeout=10):
    for digit in digits:
        click_asset(digit, confidence=confidence, timeout=timeout)


def run():
    print("Cambiando a AnyDesk")

    open_anydesk()

    wait_asset("login_button.png", confidence=0.25, timeout=15)
    click_asset("login_button.png", confidence=0.25, timeout=10)

    wait_asset("user_field.png", confidence=0.25, timeout=15)
    save_screenshot("01_login_error_form")

    click_asset("user_field.png", confidence=0.25, timeout=10)
    click_digits(INVALID_USER)

    click_asset("pass_field.png", confidence=0.25, timeout=10)
    click_digits(INVALID_PASSWORD)

    save_screenshot("02_login_error_credentials")

    click_asset("entry_button.png", confidence=0.25, timeout=10)

    wait_asset("login_error.png", confidence=0.25, timeout=20)
    save_screenshot("03_login_error_message")

    generate_pdf_report()


if __name__ == "__main__":
    run()
