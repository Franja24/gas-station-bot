import os
import subprocess
import time

import pyautogui

from clicker import click_coordinates, double_click_coordinates
from features.platform_profile import use_windows_path
from screenshot import save_screenshot


ANYDESK_BUNDLE_ID = "com.philandro.anydesk"
RUSTDESK_BUNDLE_ID = "com.carriez.rustdesk"
REMOTE_DESKTOP_APP_ENV = "GAS_STATION_REMOTE_DESKTOP"
REMOTE_DESKTOP_COMMAND_ENV = "GAS_STATION_REMOTE_DESKTOP_COMMAND"
ANYDESK_COMMAND_ENV = "GAS_STATION_ANYDESK_COMMAND"
RUSTDESK_COMMAND_ENV = "GAS_STATION_RUSTDESK_COMMAND"
WINDOWS_APP_COMMAND_ENV = "GAS_STATION_WINDOWS_APP_COMMAND"
WINDOWS_REMOTE_DESKTOP_TITLE = "Conexión a Escritorio remoto"
RUSTDESK_WINDOWS_WINDOW_KEYWORD_ENV = "GAS_STATION_RUSTDESK_WINDOW_KEYWORD"
RUSTDESK_WINDOWS_EXECUTABLE = r"C:\Program Files\RustDesk\rustdesk.exe"

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
RUSTDESK_WINDOWS_REMOTE_WINDOW_KEYWORD = "tpv02-6588"
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
    configured_app = os.environ.get(REMOTE_DESKTOP_APP_ENV, "").strip().lower()

    if configured_app:
        return configured_app

    return "rustdesk" if use_windows_path() else "anydesk"


def _run_windows_command(command, fallback_app_name):
    resolved_command = os.environ.get(command, "").strip()

    if resolved_command:
        if os.path.isfile(resolved_command):
            subprocess.Popen([resolved_command])
        else:
            subprocess.run(resolved_command, shell=True, check=True)
        return

    if os.path.isfile(fallback_app_name):
        subprocess.Popen([fallback_app_name])
        return

    subprocess.run(["cmd", "/c", "start", "", fallback_app_name], check=True)


def _windows_remote_window_keyword(app_key):
    if app_key != "rustdesk":
        return ""

    return os.environ.get(
        RUSTDESK_WINDOWS_WINDOW_KEYWORD_ENV,
        RUSTDESK_WINDOWS_REMOTE_WINDOW_KEYWORD,
    ).strip()


def _foreground_windows_window_title():
    import ctypes

    window_handle = ctypes.windll.user32.GetForegroundWindow()
    title_length = ctypes.windll.user32.GetWindowTextLengthW(window_handle)
    title_buffer = ctypes.create_unicode_buffer(title_length + 1)
    ctypes.windll.user32.GetWindowTextW(
        window_handle,
        title_buffer,
        title_length + 1,
    )

    return title_buffer.value


def _release_windows_remote_desktop_focus(app_key):
    if app_key != "rustdesk":
        return

    foreground_title = _foreground_windows_window_title()

    if WINDOWS_REMOTE_DESKTOP_TITLE.lower() not in foreground_title.lower():
        return

    print("[INFO] Liberando el foco local de Escritorio remoto...")
    pyautogui.hotkey("alt", "tab")
    time.sleep(1)


def _activate_matching_windows_window(app_key):
    keyword = _windows_remote_window_keyword(app_key)

    if not keyword:
        return False

    try:
        import pygetwindow
    except ImportError:
        print("[WARN] pygetwindow no esta disponible para activar ventanas.")
        return False

    matching_windows = [
        window
        for window in pygetwindow.getAllWindows()
        if keyword.lower() in window.title.lower()
    ]

    if not matching_windows:
        return False

    # RustDesk suele dejar la ventana principal encima; preferimos una ventana
    # remota visible por titulo, por ejemplo "370945606@tpv02-6588".
    remote_window = matching_windows[0]

    _release_windows_remote_desktop_focus(app_key)

    if remote_window.isMinimized:
        remote_window.restore()

    try:
        remote_window.activate()
    except Exception as exc:
        print(f"[WARN] Activación directa falló: {exc}. Reintentando.")
        remote_window.minimize()
        time.sleep(0.3)
        remote_window.restore()
        time.sleep(0.5)
        remote_window.activate()
    time.sleep(1)
    save_screenshot("rustdesk_remote_window_opened")
    print(f"[OK] RustDesk sesion activa en Windows: {remote_window.title}")

    return True


def _launch_remote_desktop_windows(app_key):
    app_config = REMOTE_DESKTOP_APPS[app_key]
    display_name = app_config["frontmost_name"]
    screenshot_slug = app_config["screenshot_slug"]

    if app_key == "anydesk":
        command_env = ANYDESK_COMMAND_ENV
        fallback_command = display_name
    elif app_key == "rustdesk":
        command_env = RUSTDESK_COMMAND_ENV
        fallback_command = RUSTDESK_WINDOWS_EXECUTABLE
    else:
        command_env = REMOTE_DESKTOP_COMMAND_ENV
        fallback_command = display_name

    if _activate_matching_windows_window(app_key):
        return

    print(f"[INFO] Abriendo {display_name} en Windows...")
    _run_windows_command(command_env, fallback_command)
    time.sleep(3)
    if _activate_matching_windows_window(app_key):
        return

    save_screenshot(f"{screenshot_slug}_opened")
    print(f"[OK] {display_name} lanzado en Windows")


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

    if use_windows_path():
        _launch_remote_desktop_windows(selected_app)
        return

    _open_remote_desktop(selected_app)


def open_rustdesk():
    use_remote_desktop("rustdesk")
    open_anydesk()


def open_windows_app():
    print("[INFO] Abriendo Escritorio remoto...")

    if use_windows_path():
        try:
            import pygetwindow
        except ImportError:
            pygetwindow = None

        if pygetwindow is not None:
            matching_windows = [
                window
                for window in pygetwindow.getAllWindows()
                if WINDOWS_REMOTE_DESKTOP_TITLE.lower() in window.title.lower()
            ]
            if matching_windows:
                remote_window = matching_windows[0]
                if remote_window.isMinimized:
                    remote_window.restore()
                try:
                    remote_window.activate()
                except Exception as exc:
                    print(f"[WARN] Activación directa falló: {exc}. Reintentando.")
                    remote_window.minimize()
                    time.sleep(0.3)
                    remote_window.restore()
                    time.sleep(0.5)
                    remote_window.activate()
                time.sleep(1)
                save_screenshot("windows_remote_desktop_opened")
                print(f"[OK] Escritorio remoto activo: {remote_window.title}")
                return

        _run_windows_command(WINDOWS_APP_COMMAND_ENV, "mstsc.exe")
    else:
        subprocess.run(["open", "-a", "Windows App"], check=True)

    time.sleep(5)
    save_screenshot("windows_remote_desktop_opened")
    print("[OK] Escritorio remoto abierto")
