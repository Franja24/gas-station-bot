import time

import pyautogui

from features.applications import open_windows_app
from screenshot import save_screenshot, generate_pdf_report


def run(generate_report=True):
    print("[WINDOWS APP] Cerrando/descolgando simulador de bomba")

    open_windows_app()
    time.sleep(2)

    pyautogui.press("c")
    save_screenshot("windows_app_close_executed")

    if generate_report:
        generate_pdf_report()


if __name__ == "__main__":
    run()
