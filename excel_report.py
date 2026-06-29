from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


REPORT_HEADERS = ["ID del caso", "Estatus", "Descripción", "Día", "Hora"]


def _cell_ref(row_number, column_number):
    column_name = ""

    while column_number:
        column_number, remainder = divmod(column_number - 1, 26)
        column_name = chr(65 + remainder) + column_name

    return f"{column_name}{row_number}"


def _inline_string_cell(row_number, column_number, value, style_id=None):
    style = f' s="{style_id}"' if style_id is not None else ""
    text = escape("" if value is None else str(value))

    return (
        f'<c r="{_cell_ref(row_number, column_number)}" t="inlineStr"{style}>'
        f"<is><t>{text}</t></is></c>"
    )


def _number_cell(row_number, column_number, value, style_id=None):
    style = f' s="{style_id}"' if style_id is not None else ""

    return f'<c r="{_cell_ref(row_number, column_number)}"{style}><v>{value}</v></c>'


def _row_xml(row_number, values, style_id=None, row_height=None):
    height = ""
    if row_height is not None:
        height = f' ht="{row_height}" customHeight="1"'

    cells = []
    for index, value in enumerate(values, start=1):
        if isinstance(value, (int, float)):
            cells.append(_number_cell(row_number, index, value, style_id))
        else:
            cells.append(_inline_string_cell(row_number, index, value, style_id))

    return f'<row r="{row_number}"{height}>{"".join(cells)}</row>'


def _split_datetime(value):
    if not value:
        return "", ""

    day, _, time = value.partition("T")

    return day, time


def _case_description(case):
    failed_stage = next(
        (
            stage
            for stage in case.get("stages", [])
            if stage.get("status") == "FAILED"
        ),
        None,
    )

    prefix = ""
    if not case.get("reportable", True):
        prefix = "Limpieza auxiliar. "

    if failed_stage:
        error = failed_stage.get("error") or case.get("error") or ""
        return f"{prefix}{failed_stage.get('name', 'paso')}: {error}"

    if case.get("status") == "PASSED":
        return f"{prefix}Caso ejecutado correctamente."

    return f"{prefix}{case.get('error') or 'Caso fallido.'}"


def _report_rows(result):
    suite_cases = result.get("suite_cases") or []

    if suite_cases:
        rows = []
        for case in suite_cases:
            day, time = _split_datetime(case.get("started_at"))
            rows.append(
                [
                    case.get("name", ""),
                    case.get("status", ""),
                    _case_description(case),
                    day,
                    time,
                ]
            )

        return rows

    day, time = _split_datetime(result.get("started_at"))
    return [
        [
            result.get("case_name", ""),
            result.get("status", ""),
            _case_description(result),
            day,
            time,
        ]
    ]


def _sheet_xml(result):
    rows = _report_rows(result)
    summary = result.get("suite_summary") or {}
    auxiliary_summary = result.get("auxiliary_summary") or {}
    total = summary.get("total", len(rows))
    passed = summary.get(
        "passed",
        sum(1 for row in rows if row[1] == "PASSED"),
    )
    failed = summary.get(
        "failed",
        sum(1 for row in rows if row[1] == "FAILED"),
    )
    auxiliary_passed = auxiliary_summary.get("passed", 0)
    auxiliary_failed = auxiliary_summary.get("failed", 0)

    sheet_rows = [
        _row_xml(1, ["Reporte suite E2E"], style_id=1),
        _row_xml(3, ["Caso", result.get("case_name", "")], style_id=4),
        _row_xml(4, ["Resultado", result.get("status", "")], style_id=4),
        _row_xml(5, ["Total funcional", total], style_id=4),
        _row_xml(
            6,
            ["Pasaron / Fallaron funcionales", f"{passed} / {failed}"],
            style_id=4,
        ),
        _row_xml(
            7,
            ["Limpiezas", f"{auxiliary_passed} / {auxiliary_failed}"],
            style_id=4,
        ),
        _row_xml(8, REPORT_HEADERS, style_id=1),
    ]

    for offset, row in enumerate(rows, start=9):
        style_id = 3 if row[1] == "PASSED" else 2 if row[1] == "FAILED" else None
        sheet_rows.append(_row_xml(offset, row, style_id=style_id, row_height=48))

    last_row = 8 + len(rows)

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <dimension ref="A1:E{last_row}"/>
  <sheetViews>
    <sheetView workbookViewId="0">
      <pane ySplit="8" topLeftCell="A9" activePane="bottomLeft" state="frozen"/>
      <selection pane="bottomLeft" activeCell="A9" sqref="A9"/>
    </sheetView>
  </sheetViews>
  <cols>
    <col min="1" max="1" width="22" customWidth="1"/>
    <col min="2" max="2" width="14" customWidth="1"/>
    <col min="3" max="3" width="88" customWidth="1"/>
    <col min="4" max="4" width="16" customWidth="1"/>
    <col min="5" max="5" width="13" customWidth="1"/>
  </cols>
  <sheetData>
    {"".join(sheet_rows)}
  </sheetData>
  <autoFilter ref="A8:E{last_row}"/>
</worksheet>"""


def _styles_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="4">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><sz val="12"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
    <font><b/><color rgb="FF9C0006"/><name val="Calibri"/></font>
    <font><b/><color rgb="FF375623"/><name val="Calibri"/></font>
  </fonts>
  <fills count="5">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E79"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFCE4D6"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE2F0D9"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border>
      <left style="thin"><color rgb="FFB7B7B7"/></left>
      <right style="thin"><color rgb="FFB7B7B7"/></right>
      <top style="thin"><color rgb="FFB7B7B7"/></top>
      <bottom style="thin"><color rgb="FFB7B7B7"/></bottom>
      <diagonal/>
    </border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="5">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="3" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""


def generate_excel_report(result, output_folder, run_id):
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    report_path = output_folder / "execution_report.xlsx"

    with ZipFile(report_path, "w", ZIP_DEFLATED) as workbook:
        workbook.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>""",
        )
        workbook.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>""",
        )
        workbook.writestr(
            "xl/workbook.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets><sheet name="Reporte" sheetId="1" r:id="rId1"/></sheets>
</workbook>""",
        )
        workbook.writestr(
            "xl/_rels/workbook.xml.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>""",
        )
        workbook.writestr("xl/worksheets/sheet1.xml", _sheet_xml(result))
        workbook.writestr("xl/styles.xml", _styles_xml())
        workbook.writestr(
            "docProps/core.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Reporte suite E2E {escape(run_id)}</dc:title>
  <dc:creator>Gas Station Automation Bot</dc:creator>
</cp:coreProperties>""",
        )
        workbook.writestr(
            "docProps/app.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Gas Station Automation Bot</Application>
</Properties>""",
        )

    print(f"[OK] Excel generado: {report_path.resolve()}")

    return report_path
