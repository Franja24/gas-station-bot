from datetime import datetime
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

import pyautogui

from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
)

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet


RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")

RUN_FOLDER = Path(__file__).resolve().parent / "Evidencias" / f"run_{RUN_ID}"

SCREENSHOTS_FOLDER = RUN_FOLDER / "screenshots"

_CURRENT_STAGE = None
_CURRENT_CASE = None


def start_run(run_id=None):
    global RUN_ID, RUN_FOLDER, SCREENSHOTS_FOLDER, _CURRENT_STAGE, _CURRENT_CASE

    RUN_ID = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    RUN_FOLDER = Path(__file__).resolve().parent / "Evidencias" / f"run_{RUN_ID}"
    SCREENSHOTS_FOLDER = RUN_FOLDER / "screenshots"
    _CURRENT_STAGE = None
    _CURRENT_CASE = None

    return RUN_FOLDER


def set_screenshot_stage(stage_name):
    global _CURRENT_STAGE
    _CURRENT_STAGE = stage_name


def set_screenshot_case(case_id):
    global _CURRENT_CASE
    _CURRENT_CASE = case_id


def save_screenshot(name):
    SCREENSHOTS_FOLDER.mkdir(parents=True, exist_ok=True)

    prefix_parts = []
    if _CURRENT_CASE:
        prefix_parts.append(_CURRENT_CASE)
    if _CURRENT_STAGE:
        prefix_parts.append(_CURRENT_STAGE)
    prefix_parts.append(name)
    screenshot_name = "__".join(prefix_parts)
    filename = SCREENSHOTS_FOLDER / f"{screenshot_name}.png"

    # Pillow no siempre puede escribir rutas que rebasan el límite clásico de
    # Windows. Conservamos la parte legible y añadimos un hash para evitar
    # colisiones entre casos/etapas con nombres largos.
    if len(str(filename)) >= 240:
        digest = hashlib.sha1(screenshot_name.encode("utf-8")).hexdigest()[:10]
        available = max(40, 230 - len(str(SCREENSHOTS_FOLDER)))
        readable = screenshot_name[: max(20, available - len(digest) - 2)]
        filename = SCREENSHOTS_FOLDER / f"{readable}__{digest}.png"

    screenshot = pyautogui.screenshot()

    screenshot.save(str(filename))

    print(f"[OK] Screenshot guardado: {filename.resolve()}")

    return filename


def save_result(result):
    RUN_FOLDER.mkdir(parents=True, exist_ok=True)

    result_path = RUN_FOLDER / "result.json"

    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"[RESULT] Resultado guardado: {result_path.resolve()}")

    return result_path


def _case_label(test_case):
    case_id = test_case.get("id")
    case_name = test_case.get("name") or test_case.get("flow") or ""

    if case_id and case_name:
        return f"{case_id} - {case_name}"
    return case_id or case_name or "Caso"


def _stage_line(stage):
    return (
        f"{escape(stage.get('name', 'stage'))}: "
        f"{escape(stage.get('status', 'UNKNOWN'))} "
        f"({stage.get('duration_seconds', 0)} seconds)"
    )


def _status_color(status):
    if status == "PASSED":
        return colors.green
    if status == "FAILED":
        return colors.red
    return colors.orange


def _add_stage_list(elements, styles, stages, style_prefix):
    for index, stage in enumerate(stages, start=1):
        stage_status = stage.get("status", "UNKNOWN")
        stage_color = _status_color(stage_status)
        stage_style = ParagraphStyle(
            f"{style_prefix}-{index}",
            parent=styles["Normal"],
            leftIndent=18,
            textColor=stage_color,
        )
        elements.append(Paragraph(_stage_line(stage), stage_style))


def generate_pdf_report(result=None):
    RUN_FOLDER.mkdir(parents=True, exist_ok=True)

    pdf_path = RUN_FOLDER / "execution_report.pdf"

    doc = SimpleDocTemplate(str(pdf_path))

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        f"Automation Execution Report - {RUN_ID}",
        styles["Title"]
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    if result is not None:
        status = result["status"]
        status_color = _status_color(status)
        status_style = ParagraphStyle(
            "Status",
            parent=styles["Heading1"],
            textColor=status_color,
        )

        elements.append(Paragraph(f"Result: {escape(status)}", status_style))
        elements.append(
            Paragraph(
                f"Case: {escape(result['case_name'])}",
                styles["Normal"],
            )
        )
        elements.append(
            Paragraph(
                f"Duration: {result['duration_seconds']} seconds",
                styles["Normal"],
            )
        )

        if result.get("error"):
            elements.append(
                Paragraph(
                    f"Error: {escape(result['error'])}",
                    styles["Normal"],
                )
            )

        elements.append(Spacer(1, 20))

        background_stages = result.get("background_stages") or []
        test_cases = result.get("test_cases") or []

        if background_stages:
            elements.append(Paragraph("Background", styles["Heading2"]))
            _add_stage_list(elements, styles, background_stages, "Background")
            elements.append(Spacer(1, 12))

        if test_cases:
            elements.append(Paragraph("Test Cases", styles["Heading2"]))

            for case_index, test_case in enumerate(test_cases, start=1):
                case_status = test_case.get("status", "UNKNOWN")
                case_color = _status_color(case_status)
                case_style = ParagraphStyle(
                    f"TestCase-{case_index}",
                    parent=styles["Heading3"],
                    textColor=case_color,
                )
                elements.append(
                    Paragraph(
                        f"{escape(_case_label(test_case))}: {escape(case_status)} "
                        f"({test_case.get('duration_seconds', 0)} seconds)",
                        case_style,
                    )
                )
                _add_stage_list(
                    elements,
                    styles,
                    test_case.get("stages", []),
                    f"TestCase-{case_index}-Stage",
                )
                elements.append(Spacer(1, 8))

            elements.append(Spacer(1, 12))

        elif result.get("stages"):
            elements.append(Paragraph("Stages", styles["Heading2"]))
            _add_stage_list(elements, styles, result["stages"], "Stage")
            elements.append(Spacer(1, 20))

    screenshots = sorted(
        SCREENSHOTS_FOLDER.glob("*.png"),
        key=lambda x: x.name,
    )


    for screenshot in screenshots:

        step_name = screenshot.stem

        elements.append(
            Paragraph(
                step_name,
                styles["Heading2"]
            )
        )

        elements.append(
            Image(
                str(screenshot),
                width=400,
                height=225
            )
        )

        elements.append(Spacer(1, 20))

    doc.build(elements)

    print(f"[OK] PDF generado: {pdf_path.resolve()}")

    return pdf_path
