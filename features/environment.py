import re
import time
from datetime import datetime

import screenshot
from excel_report import generate_excel_report
from pos_log_collector import (
    copy_latest_pos_log_to_run_folder,
    is_pos_log_after_run_enabled,
)


def _scenario_slug(scenario):
    slug = re.sub(r"[^A-Za-z0-9]+", "_", scenario.name).strip("_").lower()
    return slug[:60] or "scenario"


def _status_name(scenario):
    status = getattr(scenario, "status", None)
    return getattr(status, "name", str(status)).upper()


def before_scenario(context, scenario):
    run_id = (
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        f"_behave_{_scenario_slug(scenario)}"
    )
    screenshot.start_run(run_id)

    context.behave_scenario_started_at = datetime.now()
    context.behave_scenario_started_time = time.monotonic()
    context.behave_stages = []
    context.behave_background_stages = []
    context.behave_test_cases = []
    context.behave_error = None
    context.behave_step_sequence = 0

    print(f"[BEHAVE] Evidencia: {screenshot.RUN_FOLDER.resolve()}")


def before_step(context, step):
    context.behave_step_sequence = getattr(context, "behave_step_sequence", 0) + 1
    keyword = re.sub(r"[^A-Za-z0-9]+", "_", step.keyword).strip("_").lower()
    name = re.sub(r"[^A-Za-z0-9]+", "_", step.name).strip("_").lower()
    screenshot.set_screenshot_stage(
        f"{context.behave_step_sequence:02d}_{keyword}_{name}"
    )


def after_scenario(context, scenario):
    finished_at = datetime.now()
    started_at = getattr(context, "behave_scenario_started_at", finished_at)
    started_time = getattr(context, "behave_scenario_started_time", time.monotonic())
    status = _status_name(scenario)
    error = getattr(context, "behave_error", None)

    if status != "PASSED" and error is None:
        error = f"Behave scenario ended with status {status}"

    if status != "PASSED":
        try:
            screenshot.set_screenshot_stage("99_scenario_result")
            screenshot.save_screenshot("FAILED_error")
        except Exception as screenshot_error:
            print(f"[WARN] No se pudo guardar captura del fallo: {screenshot_error}")

    result = {
        "run_id": screenshot.RUN_ID,
        "case_name": scenario.name,
        "status": status,
        "started_at": started_at.isoformat(timespec="seconds"),
        "finished_at": finished_at.isoformat(timespec="seconds"),
        "duration_seconds": round(time.monotonic() - started_time, 2),
        "error": error,
        "traceback": None,
        "stages": getattr(context, "behave_stages", []),
        "background_stages": getattr(context, "behave_background_stages", []),
        "test_cases": getattr(context, "behave_test_cases", []),
        "pass_criteria": (
            "Behave scenario completed without failed steps and all configured "
            "functional validations passed."
        ),
    }

    if is_pos_log_after_run_enabled():
        try:
            copied_log = copy_latest_pos_log_to_run_folder(
                run_folder=screenshot.RUN_FOLDER,
            )
            if copied_log is not None:
                result["pos_log"] = copied_log.name
        except Exception as log_error:
            print(f"[WARN] No se pudo anexar el log POS: {log_error}")

    screenshot.save_result(result)
    generate_excel_report(result, screenshot.RUN_FOLDER, screenshot.RUN_ID)
    screenshot.generate_pdf_report(result)
    screenshot.set_screenshot_stage(None)
