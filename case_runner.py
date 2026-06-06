import time
import traceback
from datetime import datetime

from screenshot import (
    RUN_FOLDER,
    RUN_ID,
    generate_pdf_report,
    save_result,
    save_screenshot,
    set_screenshot_stage,
)


class StageExecutionError(RuntimeError):
    def __init__(self, stage_name, stages, original_error):
        super().__init__(
            f"Stage {stage_name} failed: "
            f"{type(original_error).__name__}: {original_error}"
        )
        self.stage_name = stage_name
        self.stages = stages
        self.original_error = original_error


def run_stages(stages):
    stage_results = []

    for stage_name, stage_function in stages:
        started_at = datetime.now()
        start_time = time.monotonic()
        set_screenshot_stage(stage_name)

        print("")
        print("-" * 60)
        print(f"[STAGE] Iniciando: {stage_name}")
        print("-" * 60)

        try:
            stage_function()
        except Exception as exc:
            duration_seconds = round(time.monotonic() - start_time, 2)
            stage_results.append(
                {
                    "name": stage_name,
                    "status": "FAILED",
                    "started_at": started_at.isoformat(timespec="seconds"),
                    "duration_seconds": duration_seconds,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            raise StageExecutionError(stage_name, stage_results, exc) from exc
        else:
            duration_seconds = round(time.monotonic() - start_time, 2)
            stage_results.append(
                {
                    "name": stage_name,
                    "status": "PASSED",
                    "started_at": started_at.isoformat(timespec="seconds"),
                    "duration_seconds": duration_seconds,
                    "error": None,
                }
            )
            print(f"[STAGE] PASSED: {stage_name}")
        finally:
            set_screenshot_stage(None)

    return {"stages": stage_results}


def run_case(case_name, case_function):
    started_at = datetime.now()
    start_time = time.monotonic()
    error = None
    traceback_text = None
    status = "PASSED"
    case_details = {}

    print(f"[CASE] Iniciando: {case_name}")

    try:
        returned_details = case_function()
        if isinstance(returned_details, dict):
            case_details = returned_details
    except Exception as exc:
        status = "FAILED"
        error = f"{type(exc).__name__}: {exc}"
        traceback_text = traceback.format_exc()
        if isinstance(exc, StageExecutionError):
            case_details["stages"] = exc.stages

        print(f"[CASE] FAILED: {case_name}")
        print(f"[ERROR] {error}")
        print(traceback_text)

        if isinstance(exc, StageExecutionError):
            set_screenshot_stage(exc.stage_name)

        try:
            save_screenshot("FAILED_error")
        except Exception as screenshot_error:
            print(f"[WARN] No se pudo guardar captura del fallo: {screenshot_error}")
        finally:
            set_screenshot_stage(None)

    finished_at = datetime.now()
    duration_seconds = round(time.monotonic() - start_time, 2)

    result = {
        "run_id": RUN_ID,
        "case_name": case_name,
        "status": status,
        "started_at": started_at.isoformat(timespec="seconds"),
        "finished_at": finished_at.isoformat(timespec="seconds"),
        "duration_seconds": duration_seconds,
        "error": error,
        "traceback": traceback_text,
        "stages": case_details.get("stages", []),
        "pass_criteria": (
            "Case completed without exceptions and all configured "
            "functional validations passed."
        ),
    }

    save_result(result)
    generate_pdf_report(result)

    print("")
    print("=" * 60)
    print(f"RESULTADO: {status}")
    print(f"CASO: {case_name}")
    print(f"EVIDENCIA: {RUN_FOLDER.resolve()}")
    if error:
        print(f"ERROR: {error}")
    print("=" * 60)

    return status == "PASSED"
