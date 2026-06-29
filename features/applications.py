import subprocess
import time

from screenshot import save_screenshot


def activate_process(process_name):
    subprocess.run(
        [
            "osascript",
            "-e",
            (
                'tell application "System Events" to set frontmost of '
                f'process "{process_name}" to true'
            ),
        ],
        check=True,
    )

    time.sleep(1)


def open_anydesk():
    print("[INFO] Abriendo AnyDesk...")

    subprocess.run(["open", "/Applications/AnyDesk.app"], check=True)

    time.sleep(2)

    subprocess.run(
        ["osascript", "-e", 'tell application "AnyDesk" to activate'],
        check=True
    )

    activate_process("AnyDesk")

    time.sleep(3)

    save_screenshot("anydesk_opened")

    print("[OK] AnyDesk activo")


def open_windows_app():

    print("[INFO] Abriendo Windows App...")

    subprocess.run(
        ["open", "-a", "Windows App"],
        check=True
    )

    activate_process("Windows App")

    time.sleep(5)

    save_screenshot("windows_app_opened")

    print("[OK] Windows App abierto")
