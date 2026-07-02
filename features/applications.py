import os
import subprocess
import time

from clicker import click_coordinates, double_click_coordinates
from screenshot import save_screenshot


ANYDESK_BUNDLE_ID = "com.philandro.anydesk"
RUSTDESK_BUNDLE_ID = "com.carriez.rustdesk"
REMOTE_DESKTOP_APP_ENV = "GAS_STATION_REMOTE_DESKTOP"

REMOTE_DESKTOP_APPS = {
    "anydesk": {
        "bundle_id": ANYDESK_BUNDLE_ID,
        "frontmost_name": "AnyDesk",
        "screenshot_slug": "anydesk",
    },
    "rustdesk": {
        "bundle_id": RUSTDESK_BUNDLE_ID,
        "frontmost_name": "RustDesk",
        "screenshot_slug": "rustdesk",
    },
}

RUSTDESK_REMOTE_WINDOW_KEYWORD = "KIOSCO@"
RUSTDESK_REMOTE_DESKTOP_WINDOW_SUFFIX = "Remote Desktop - RustDesk"
RUSTDESK_HOME_WINDOW_NAME = "RustDesk"
RUSTDESK_FIRST_KIOSCO_CARD_OFFSET = (375, 430)
RUSTDESK_KIOSCO_TAB_OFFSET = (180, 20)


def use_remote_desktop(app_name):
    normalized_app = app_name.strip().lower()

    if normalized_app not in REMOTE_DESKTOP_APPS:
        available_apps = ", ".join(sorted(REMOTE_DESKTOP_APPS))
        raise ValueError(
            f"Remote desktop no soportado: {app_name}. "
            f"Disponibles: {available_apps}"
        )

    os.environ[REMOTE_DESKTOP_APP_ENV] = normalized_app
    print(f"[INFO] Remote desktop seleccionado: {normalized_app}")


def _selected_remote_desktop():
    return os.environ.get(REMOTE_DESKTOP_APP_ENV, "anydesk").strip().lower()


def _activate_app(bundle_id, app_name):
    subprocess.run(["open", "-b", bundle_id], check=True)
    subprocess.run(
        [
            "osascript",
            "-e",
            f'tell application id "{bundle_id}" to activate',
        ],
        check=True,
    )
    subprocess.run(["open", "-a", app_name], check=False)
    subprocess.run(
        [
            "osascript",
            "-e",
            (
                'tell application "System Events" to tell process '
                f'"{app_name}" to set frontmost to true'
            ),
        ],
        check=False,
    )


def _frontmost_app_name():
    completed_process = subprocess.run(
        [
            "osascript",
            "-e",
            (
                'tell application "System Events" to get name of '
                "first application process whose frontmost is true"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    return completed_process.stdout.strip()


def _rustdesk_window_names():
    completed_process = subprocess.run(
        [
            "osascript",
            "-e",
            (
                'tell application "System Events" to tell process "RustDesk" '
                "to get name of windows"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    return [
        window_name.strip()
        for window_name in completed_process.stdout.strip().split(",")
        if window_name.strip()
    ]


def _raise_rustdesk_window(window_name):
    subprocess.run(
        [
            "osascript",
            "-e",
            (
                'tell application "System Events" to tell process "RustDesk" '
                f'to perform action "AXRaise" of window "{window_name}"'
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def _front_rustdesk_window_details():
    completed_process = subprocess.run(
        [
            "osascript",
            "-e",
            (
                'tell application "System Events" to tell process "RustDesk" '
                "to get {name, position, size} of front window"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    parts = [part.strip() for part in completed_process.stdout.strip().split(",")]
    if len(parts) < 5:
        raise RuntimeError(
            f"No se pudo leer la ventana frontal de RustDesk: {parts}"
        )

    return {
        "name": parts[0],
        "x": int(parts[1]),
        "y": int(parts[2]),
        "width": int(parts[3]),
        "height": int(parts[4]),
    }


def _connect_first_rustdesk_kiosco():
    window_details = _front_rustdesk_window_details()
    card_x = window_details["x"] + RUSTDESK_FIRST_KIOSCO_CARD_OFFSET[0]
    card_y = window_details["y"] + RUSTDESK_FIRST_KIOSCO_CARD_OFFSET[1]

    print("[INFO] Abriendo primera conexión KIOSCO en RustDesk...")
    double_click_coordinates(card_x, card_y)
    time.sleep(5)


def _select_rustdesk_kiosco_tab():
    window_details = _front_rustdesk_window_details()
    tab_x = window_details["x"] + RUSTDESK_KIOSCO_TAB_OFFSET[0]
    tab_y = window_details["y"] + RUSTDESK_KIOSCO_TAB_OFFSET[1]

    print("[INFO] Seleccionando pestaña KIOSCO en RustDesk...")
    click_coordinates(tab_x, tab_y)
    time.sleep(1)


def _ensure_rustdesk_remote_window():
    _activate_app(RUSTDESK_BUNDLE_ID, "RustDesk")

    for window_name in _rustdesk_window_names():
        if (
            RUSTDESK_REMOTE_WINDOW_KEYWORD in window_name
            or RUSTDESK_REMOTE_DESKTOP_WINDOW_SUFFIX in window_name
        ):
            _raise_rustdesk_window(window_name)
            time.sleep(1)
            _select_rustdesk_kiosco_tab()
            save_screenshot("rustdesk_remote_window_opened")
            print(f"[OK] RustDesk sesión activa: {window_name}")
            return

    front_window = _front_rustdesk_window_details()
    if front_window["name"] == RUSTDESK_HOME_WINDOW_NAME:
        _connect_first_rustdesk_kiosco()

        for window_name in _rustdesk_window_names():
            if (
                RUSTDESK_REMOTE_WINDOW_KEYWORD in window_name
                or RUSTDESK_REMOTE_DESKTOP_WINDOW_SUFFIX in window_name
            ):
                _raise_rustdesk_window(window_name)
                time.sleep(1)
                _select_rustdesk_kiosco_tab()
                save_screenshot("rustdesk_remote_window_opened")
                print(f"[OK] RustDesk sesión activa: {window_name}")
                return

    save_screenshot("rustdesk_remote_window_not_found")
    raise RuntimeError("No se pudo abrir la sesión KIOSCO en RustDesk")


def _open_remote_desktop(app_key):
    if app_key == "rustdesk":
        print("[INFO] Abriendo RustDesk...")
        _ensure_rustdesk_remote_window()
        return

    app_config = REMOTE_DESKTOP_APPS[app_key]
    display_name = app_config["frontmost_name"]
    screenshot_slug = app_config["screenshot_slug"]
    frontmost_app = None

    print(f"[INFO] Abriendo {display_name}...")

    _activate_app(app_config["bundle_id"], display_name)

    started_at = time.monotonic()
    while time.monotonic() - started_at < 10:
        time.sleep(1)

        frontmost_app = _frontmost_app_name()
        if frontmost_app == display_name:
            save_screenshot(f"{screenshot_slug}_opened")
            print(f"[OK] {display_name} activo")
            return

    save_screenshot(f"{screenshot_slug}_not_frontmost")
    raise RuntimeError(
        f"No se pudo activar {display_name}; app al frente: {frontmost_app}"
    )


def open_anydesk():
    selected_app = _selected_remote_desktop()

    if selected_app not in REMOTE_DESKTOP_APPS:
        raise ValueError(f"Remote desktop no soportado: {selected_app}")

    _open_remote_desktop(selected_app)


def open_windows_app():

    print("[INFO] Abriendo Windows App...")

    subprocess.run(
        ["open", "-a", "Windows App"],
        check=True
    )

    time.sleep(5)

    save_screenshot("windows_app_opened")

    print("[OK] Windows App abierto")
