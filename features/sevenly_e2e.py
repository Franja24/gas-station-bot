from features.login import run as login_run
from features.sevenly_login import run as sevenly_login_run
from features.magna import run as magna_run
from features.windows_app import run as windows_run
from features.invoice import run as invoice_run


def run():
    login_run()
    sevenly_login_run()
    magna_run()
    windows_run()
    invoice_run()