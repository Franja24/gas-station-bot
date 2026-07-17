import os
import sys


AUTOMATION_PLATFORM_ENV = "GAS_STATION_AUTOMATION_PLATFORM"


def get_automation_platform():
    value = os.environ.get(AUTOMATION_PLATFORM_ENV, "").strip().lower()

    if value in {"windows", "win"}:
        return "windows"

    if value in {"mac", "darwin", "osx", "macos"}:
        return "mac"

    if os.name == "nt" or sys.platform.startswith("win"):
        return "windows"

    return "mac"


def use_windows_path():
    return get_automation_platform() == "windows"
