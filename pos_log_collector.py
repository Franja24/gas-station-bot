import argparse
import os
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
EVIDENCE_ROOT = PROJECT_ROOT / "Evidencias"

POS_LOG_AFTER_RUN_ENV = "POS_LOG_AFTER_RUN"
POS_LOG_SOURCE_DIR_ENV = "POS_LOG_SOURCE_DIR"
POS_LOG_PATTERN_ENV = "POS_LOG_PATTERN"
POS_LOG_ALLOW_UNVERIFIED_SOURCE_ENV = "POS_LOG_ALLOW_UNVERIFIED_SOURCE"
POS_LOG_EXPECTED_DATE_ENV = "POS_LOG_EXPECTED_DATE"

EXPECTED_REMOTE_SOURCE_DIR = (
    "C:/Users/Tpv-xx xxxxx/AppData/Roaming/"
    "com.iconn.zimble/pos_build_petro"
)
EXPECTED_SOURCE_FOLDER_NAME = "pos_build_petro"
DEFAULT_SOURCE_DIR = PROJECT_ROOT / EXPECTED_SOURCE_FOLDER_NAME
DEFAULT_LOG_PATTERN = "api_log*"


def _expand_path(path):
    return Path(os.path.expandvars(str(path))).expanduser()


def _env_is_enabled(name):
    return os.environ.get(name, "").strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
        "si",
    }


def is_pos_log_after_run_enabled():
    return (
        _env_is_enabled(POS_LOG_AFTER_RUN_ENV)
        or bool(os.environ.get(POS_LOG_SOURCE_DIR_ENV))
    )


def get_default_source_dir():
    return _expand_path(os.environ.get(POS_LOG_SOURCE_DIR_ENV, DEFAULT_SOURCE_DIR))


def get_log_pattern():
    return os.environ.get(POS_LOG_PATTERN_ENV, DEFAULT_LOG_PATTERN)


def get_expected_log_date(run_folder=None):
    env_value = os.environ.get(POS_LOG_EXPECTED_DATE_ENV, "").strip()

    if env_value:
        return env_value

    if run_folder is None:
        return None

    run_name = Path(run_folder).name

    if not run_name.startswith("run_") or len(run_name) < 12:
        return None

    date_value = run_name[4:12]

    if not date_value.isdigit():
        return None

    return f"{date_value[:4]}-{date_value[4:6]}-{date_value[6:8]}"


def is_unverified_source_allowed():
    return _env_is_enabled(POS_LOG_ALLOW_UNVERIFIED_SOURCE_ENV)


def _source_folder_name(path):
    normalized_path = str(path).replace("\\", "/").rstrip("/")
    return normalized_path.rsplit("/", 1)[-1].lower()


def is_expected_pos_log_source(source_dir):
    return _source_folder_name(source_dir) == EXPECTED_SOURCE_FOLDER_NAME


def print_unverified_source_warning(source_dir):
    print(
        "[POS LOG] Origen rechazado para evitar copiar un log equivocado: "
        f"{source_dir}"
    )
    print(
        "[POS LOG] El log correcto esta dentro del equipo remoto de AnyDesk en: "
        f"{EXPECTED_REMOTE_SOURCE_DIR}"
    )
    print(
        "[POS LOG] Python no puede leer esa ruta C:/ directamente desde el Mac; "
        "primero transfiere el api_log* con AnyDesk."
    )
    print(
        "[POS LOG] Descargalo en una carpeta local llamada "
        f"{EXPECTED_SOURCE_FOLDER_NAME}, por ejemplo: {DEFAULT_SOURCE_DIR}"
    )


def find_latest_run_folder(evidence_root=None):
    if evidence_root is None:
        evidence_root = EVIDENCE_ROOT

    evidence_root = Path(evidence_root)
    run_folders = [
        path
        for path in evidence_root.glob("run_*")
        if path.is_dir()
    ]

    if not run_folders:
        return None

    return max(run_folders, key=lambda path: path.name)


def find_latest_pos_log(source_dir=None, pattern=None):
    source_dir = get_default_source_dir() if source_dir is None else _expand_path(source_dir)
    pattern = get_log_pattern() if pattern is None else pattern

    if (
        not is_expected_pos_log_source(source_dir)
        and not is_unverified_source_allowed()
    ):
        print_unverified_source_warning(source_dir)
        return None

    if not source_dir.is_dir():
        return None

    log_files = [
        path
        for path in source_dir.glob(pattern)
        if path.is_file()
    ]

    if not log_files:
        return None

    return max(log_files, key=lambda path: path.stat().st_mtime)


def find_expected_pos_log(source_dir=None, pattern=None, expected_date=None):
    source_dir = get_default_source_dir() if source_dir is None else _expand_path(source_dir)
    pattern = get_log_pattern() if pattern is None else pattern

    if (
        not is_expected_pos_log_source(source_dir)
        and not is_unverified_source_allowed()
    ):
        print_unverified_source_warning(source_dir)
        return None

    if not source_dir.is_dir():
        return None

    log_files = [
        path
        for path in source_dir.glob(pattern)
        if path.is_file()
    ]

    if not log_files:
        return None

    if expected_date:
        dated_logs = [
            path
            for path in log_files
            if path.name.startswith(f"api_log_{expected_date}")
        ]

        if not dated_logs:
            print(
                "[POS LOG] No se encontro log de la fecha esperada "
                f"{expected_date} en: {source_dir}"
            )
            return None

        return max(dated_logs, key=lambda path: path.stat().st_mtime)

    return max(log_files, key=lambda path: path.stat().st_mtime)


def copy_latest_pos_log_to_run_folder(
    source_dir=None,
    run_folder=None,
    pattern=None,
):
    if run_folder is None:
        run_folder = find_latest_run_folder()
    else:
        run_folder = Path(run_folder)

    if run_folder is None:
        print(f"[POS LOG] No se encontro carpeta run_* en: {EVIDENCE_ROOT}")
        return None

    expected_date = get_expected_log_date(run_folder=run_folder)
    source_path = find_expected_pos_log(
        source_dir=source_dir,
        pattern=pattern,
        expected_date=expected_date,
    )

    if source_path is None:
        source_dir = get_default_source_dir() if source_dir is None else _expand_path(source_dir)
        print(f"[POS LOG] No se encontro log en: {source_dir}")
        return None

    run_folder.mkdir(parents=True, exist_ok=True)
    destination_path = run_folder / source_path.name

    if source_path.resolve() == destination_path.resolve():
        print(f"[POS LOG] Log ya esta en el reporte: {destination_path.resolve()}")
        return destination_path

    shutil.copy2(source_path, destination_path)

    print(f"[POS LOG] Log copiado al reporte: {destination_path.resolve()}")

    return destination_path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Copia el api_log de POS correspondiente al reporte run_*."
    )
    parser.add_argument(
        "--source-dir",
        default=None,
        help=(
            "Carpeta local espejo donde AnyDesk descargo el log remoto de "
            f"{EXPECTED_REMOTE_SOURCE_DIR}. "
            f"Default: {DEFAULT_SOURCE_DIR}."
        ),
    )
    parser.add_argument(
        "--run-folder",
        default=None,
        help="Carpeta run_* destino. Default: la mas reciente en Evidencias.",
    )
    parser.add_argument(
        "--pattern",
        default=None,
        help="Patron del log. Default: api_log*.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    copied_path = copy_latest_pos_log_to_run_folder(
        source_dir=args.source_dir,
        run_folder=args.run_folder,
        pattern=args.pattern,
    )

    raise SystemExit(0 if copied_path else 1)
