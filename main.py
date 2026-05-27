import time
from clicker import click_image
from detector import find_image


def wait_for(image, timeout=15):

    result = find_image(image, timeout=timeout)

    if result is None:
        print(f"[ERROR] No apareció: {image}")
        return False

    print(f"[OK] Detectado: {image}")
    return True


def run_bot():

    print("=== INICIANDO BOT ===")

    # STEP 1
    if not click_image("iniciar.png"):
        return

    # Esperar siguiente pantalla
    if not wait_for("premium.png"):
        return

    time.sleep(1)

    # STEP 2
    if not click_image("premium.png"):
        return

    # Esperar montos
    if not wait_for("monto_500.png"):
        return

    time.sleep(1)

    # STEP 3
    if not click_image("monto_500.png"):
        return

    time.sleep(1)

    # STEP 4
    if not click_image("continuar.png"):
        return

    # Esperar sevenly
    if not wait_for("no_beneficios.png"):
        return

    time.sleep(1)

    # STEP 5
    if not click_image("no_beneficios.png"):
        return

    # Esperar pago exitoso
    if not wait_for("pago_exitoso.png", timeout=20):
        return

    print("=== PAGO EXITOSO ===")


if __name__ == "__main__":
    run_bot()