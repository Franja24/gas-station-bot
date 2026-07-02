import re
import time
from datetime import datetime

import screenshot


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
    context.behave_error = None

    print(f"[BEHAVE] Evidencia: {screenshot.RUN_FOLDER.resolve()}")


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
        "pass_criteria": (
            "Behave scenario completed without failed steps and all configured "
            "functional validations passed."
        ),
    }

    screenshot.save_result(result)
    screenshot.generate_pdf_report(result)
