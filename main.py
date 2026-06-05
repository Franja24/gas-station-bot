from features.premium import run as premium_run
from features.windows_app import run as windows_run
from features.invoice import run as invoice_run
from features.login import run as login_run

if __name__ == "__main__":

    #login
    login_run()

    # POS / Sevenly
    premium_run()

    # Simulador de bomba
    windows_run()

    #invoice system
    invoice_run()