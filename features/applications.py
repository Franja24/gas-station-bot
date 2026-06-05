import subprocess
import time

from screenshot import save_screenshot


def open_anydesk():
    print("[INFO] Abriendo AnyDesk...")

    subprocess.run(["open", "/Applications/AnyDesk.app"], check=True)

    time.sleep(2)

    subprocess.run(
        ["osascript", "-e", 'tell application "AnyDesk" to activate'],
        check=True
    )

    time.sleep(3)

    save_screenshot("anydesk_opened")

    print("[OK] AnyDesk activo")


def open_windows_app():

    print("[INFO] Abriendo Windows App...")

    subprocess.run(
        ["open", "-a", "Windows App"],
        check=True
    )

    time.sleep(5)

    save_screenshot("windows_app_opened")

    print("[OK] Windows App abierto")