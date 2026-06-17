from features.invoice import run as invoice_run
from features.login import run as login_run
from features.premium import run as premium_run
from features.windows_app import run as windows_app_run


def run():
    print("[SEVENLY] Ejecutando flujo completo")

    login_run()
    premium_run()
    windows_app_run()
    invoice_run()
