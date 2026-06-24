from datetime import datetime
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
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


def _excel_column_name(column_index):
    name = ""

    while column_index:
        column_index, remainder = divmod(column_index - 1, 26)
        name = chr(65 + remainder) + name

    return name


def _excel_cell(value, row_index, column_index):
    cell_reference = f"{_excel_column_name(column_index)}{row_index}"

    if value is None:
        value = ""

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{cell_reference}"><v>{value}</v></c>'

    text = escape(str(value))

    return (
        f'<c r="{cell_reference}" t="inlineStr">'
        f"<is><t>{text}</t></is>"
        "</c>"
    )


def _worksheet_xml(rows):
    sheet_rows = []

    for row_index, row in enumerate(rows, start=1):
        cells = [
            _excel_cell(value, row_index, column_index)
            for column_index, value in enumerate(row, start=1)
        ]
        sheet_rows.append(
            f'<row r="{row_index}">{"".join(cells)}</row>'
        )

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/'
        'spreadsheetml/2006/main">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData>'
        "</worksheet>"
    )


def _suite_case_rows(result):
    rows = [
        [
            "Case",
            "Status",
            "Started At",
            "Duration Seconds",
            "Error",
        ]
    ]

    for suite_case in result.get("suite_cases", []):
        rows.append(
            [
                suite_case.get("name"),
                suite_case.get("status"),
                suite_case.get("started_at"),
                suite_case.get("duration_seconds"),
                suite_case.get("error"),
            ]
        )

    if len(rows) == 1:
        rows.append(
            [
                result.get("case_name"),
                result.get("status"),
                result.get("started_at"),
                result.get("duration_seconds"),
                result.get("error"),
            ]
        )

    return rows


def _stage_rows(result):
    rows = [
        [
            "Case",
            "Stage",
            "Status",
            "Started At",
            "Duration Seconds",
            "Error",
        ]
    ]

    suite_cases = result.get("suite_cases", [])

    if suite_cases:
        for suite_case in suite_cases:
            for stage in suite_case.get("stages", []):
                rows.append(
                    [
                        suite_case.get("name"),
                        stage.get("name"),
                        stage.get("status"),
                        stage.get("started_at"),
                        stage.get("duration_seconds"),
                        stage.get("error"),
                    ]
                )
    else:
        for stage in result.get("stages", []):
            rows.append(
                [
                    result.get("case_name"),
                    stage.get("name"),
                    stage.get("status"),
                    stage.get("started_at"),
                    stage.get("duration_seconds"),
                    stage.get("error"),
                ]
            )

    return rows


def generate_excel_report(result):
    RUN_FOLDER.mkdir(parents=True, exist_ok=True)

    excel_path = RUN_FOLDER / "execution_report.xlsx"
    suite_summary = result.get("suite_summary") or {}

    summary_rows = [
        ["Run ID", result.get("run_id")],
        ["Case Name", result.get("case_name")],
        ["Status", result.get("status")],
        ["Started At", result.get("started_at")],
        ["Finished At", result.get("finished_at")],
        ["Duration Seconds", result.get("duration_seconds")],
        ["Error", result.get("error")],
        ["Suite Total", suite_summary.get("total", "")],
        ["Suite Passed", suite_summary.get("passed", "")],
        ["Suite Failed", suite_summary.get("failed", "")],
    ]

    worksheets = [
        ("Summary", summary_rows),
        ("Cases", _suite_case_rows(result)),
        ("Stages", _stage_rows(result)),
    ]

    with ZipFile(excel_path, "w", ZIP_DEFLATED) as workbook:
        workbook.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/'
            'package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            "</Types>",
        )
        workbook.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>",
        )
        workbook.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            "<sheets>"
            '<sheet name="Summary" sheetId="1" r:id="rId1"/>'
            '<sheet name="Cases" sheetId="2" r:id="rId2"/>'
            '<sheet name="Stages" sheetId="3" r:id="rId3"/>'
            "</sheets>"
            "</workbook>",
        )
        workbook.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>'
            "</Relationships>",
        )

        for sheet_index, (_sheet_name, rows) in enumerate(
            worksheets,
            start=1,
        ):
            workbook.writestr(
                f"xl/worksheets/sheet{sheet_index}.xml",
                _worksheet_xml(rows),
            )

    print(f"[OK] Excel generado: {excel_path.resolve()}")

    return excel_path
