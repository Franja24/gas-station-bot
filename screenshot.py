from datetime import datetime
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


def set_screenshot_stage(stage_name):
    global _CURRENT_STAGE
    _CURRENT_STAGE = stage_name


def save_screenshot(name):
    SCREENSHOTS_FOLDER.mkdir(parents=True, exist_ok=True)

    prefix = f"{_CURRENT_STAGE}__" if _CURRENT_STAGE else ""
    filename = SCREENSHOTS_FOLDER / f"{prefix}{name}.png"

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
        status_color = colors.green if status == "PASSED" else colors.red
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

        if result.get("stages"):
            elements.append(Paragraph("Stages", styles["Heading2"]))

            for stage in result["stages"]:
                stage_status = stage["status"]
                stage_color = (
                    colors.green if stage_status == "PASSED" else colors.red
                )
                stage_style = ParagraphStyle(
                    f"Stage-{stage['name']}",
                    parent=styles["Normal"],
                    textColor=stage_color,
                )
                elements.append(
                    Paragraph(
                        f"{escape(stage['name'])}: {escape(stage_status)} "
                        f"({stage['duration_seconds']} seconds)",
                        stage_style,
                    )
                )

            elements.append(Spacer(1, 20))

    screenshots = sorted(
        SCREENSHOTS_FOLDER.glob("*.png"),
        key=lambda x: x.stat().st_mtime
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
