import time

from case_runner import run_stages
from clicker import ClickError, assert_image_visible, click_coordinates, click_image
from detector import find_image
from features.applications import open_anydesk
from features.normal_magna import (
    finalize_visible_purchase_summary,
    prepare_product_selection,
)
from features.premium import handle_benefits_or_payment, wait_for_benefits_or_payment
from features.sevenly_login import run as sevenly_login_run
from features.windows_app import run as windows_run
from screenshot import save_screenshot


SUPPORTED_PRODUCTS = {
    "magna": "magna.png",
    "premium": "premium.png",
}

PRODUCT_COORDINATES = {
    "magna": (700, 398),
    "premium": (700, 256),
}

SUPPORTED_CHARGES = {
    "amount_1250": "amount_1250",
    "amount_500": "amount_500",
    "liters_20": "liters_20",
}


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


def click_asset_or_calibrated(image_name, timeout=10):
    try:
        return click_asset(image_name, timeout=timeout)
    except (ClickError, FileNotFoundError) as exc:
        print(
            f"[FALLBACK] {image_name} no se pudo usar por asset: {exc}. "
            "Intentando coordenada calibrada."
        )

        return click_calibrated(image_name, timeout=timeout)


def amount_selection_visible(timeout=2):
    return find_image("amount_1250.png", confidence=0.80, timeout=timeout) is not None


def click_product_button(product):
    product_asset = SUPPORTED_PRODUCTS[product]
    fallback_coordinates = PRODUCT_COORDINATES[product]

    for attempt in range(1, 3):
        if amount_selection_visible(timeout=1):
            return

        print(
            f"[PRODUCT] Intento {attempt}: clic por asset {product_asset}"
        )

        try:
            click_asset(product_asset, timeout=5)
        except ClickError as exc:
            print(
                f"[FALLBACK] {product_asset} no se pudo usar por asset: {exc}. "
                "Intentando coordenada calibrada."
            )
            click_coordinates(*fallback_coordinates)

        time.sleep(2)

        if amount_selection_visible(timeout=2):
            return

    click_coordinates(*fallback_coordinates)


def select_product(product):
    product_asset = SUPPORTED_PRODUCTS[product]

    open_anydesk()

    if not amount_selection_visible(timeout=2):
        assert_image_visible(product_asset, confidence=0.80, timeout=20)
        time.sleep(1)
        click_product_button(product)

    assert_image_visible("amount_1250.png", confidence=0.80, timeout=10)
    save_screenshot(f"charge_operation_{product}_selected")


def select_charge(charge_type):
    if charge_type == "amount_1250":
        click_asset("amount_1250.png", timeout=10)
        assert_image_visible("continue_button.png", confidence=0.80, timeout=10)
        save_screenshot("charge_operation_amount_1250_selected")
        return

    click_asset("amount_1250.png", timeout=10)
    time.sleep(1)

    if charge_type == "amount_500":
        click_asset_or_calibrated("charge_type_amount_tab.png", timeout=10)
        time.sleep(1)
        click_asset_or_calibrated("charge_amount_500.png", timeout=10)
        assert_image_visible("continue_button.png", confidence=0.80, timeout=10)
        save_screenshot("charge_operation_amount_500_selected")
        return

    if charge_type == "liters_20":
        click_asset_or_calibrated("charge_type_liters_tab.png", timeout=10)
        time.sleep(1)
        click_asset_or_calibrated("charge_liters_20.png", timeout=10)
        assert_image_visible("continue_button.png", confidence=0.80, timeout=10)
        save_screenshot("charge_operation_liters_20_selected")
        return

    raise ClickError(f"Tipo de carga no soportado: {charge_type}")


def complete_card_payment():
    click_asset("continue_button.png", timeout=10)

    benefits_state = wait_for_benefits_or_payment()
    save_screenshot("charge_operation_continue_clicked")

    handle_benefits_or_payment(benefits_state)

    click_asset("card.png", timeout=10)
    save_screenshot("charge_operation_wait_payment")

    assert_image_visible("payment_success.png", confidence=0.80, timeout=30)
    save_screenshot("charge_operation_payment_success")


def finalize_dispatch():
    windows_run()
    open_anydesk()
    finalize_visible_purchase_summary()


def validate_options(product, charge_type):
    if product not in SUPPORTED_PRODUCTS:
        available_products = ", ".join(sorted(SUPPORTED_PRODUCTS))
        raise ClickError(
            f"Combustible no soportado: {product}. "
            f"Disponibles: {available_products}"
        )

    if charge_type not in SUPPORTED_CHARGES:
        available_charges = ", ".join(sorted(SUPPORTED_CHARGES))
        raise ClickError(
            f"Tipo de carga no soportado: {charge_type}. "
            f"Disponibles: {available_charges}"
        )


def run(product="magna", charge_type="amount_1250", use_sevenly=False):
    validate_options(product, charge_type)

    stages = [("00_prepare_product_selection", prepare_product_selection)]

    if use_sevenly:
        stages.append(("01_sevenly_login", sevenly_login_run))

    stages.extend(
        [
            ("02_select_product", lambda: select_product(product)),
            ("03_select_charge", lambda: select_charge(charge_type)),
            ("04_complete_card_payment", complete_card_payment),
            ("05_windows_app_and_finalize", finalize_dispatch),
        ]
    )

    return run_stages(stages)
