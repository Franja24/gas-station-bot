import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from excel_report import generate_excel_report


class ExcelReportTests(unittest.TestCase):
    def test_generates_suite_report_with_description_column(self):
        result = {
            "run_id": "20260618_111728",
            "case_name": "e2e_set_5",
            "status": "FAILED",
            "suite_summary": {
                "total": 1,
                "passed": 0,
                "failed": 1,
            },
            "suite_cases": [
                {
                    "name": "01_e2e",
                    "status": "FAILED",
                    "started_at": "2026-06-18T11:17:29",
                    "error": "StageExecutionError",
                    "stages": [
                        {
                            "name": "00_open_kiosco",
                            "status": "FAILED",
                            "error": (
                                "ClickError: no apareció login_button.png"
                            ),
                        }
                    ],
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_directory:
            report_path = generate_excel_report(
                result,
                Path(temp_directory),
                "20260618_111728",
            )

            self.assertTrue(report_path.is_file())
            self.assertEqual(report_path.name, "execution_report.xlsx")

            with ZipFile(report_path) as workbook:
                sheet_xml = workbook.read(
                    "xl/worksheets/sheet1.xml"
                ).decode("utf-8")

        self.assertIn("Descripción", sheet_xml)
        self.assertIn("00_open_kiosco", sheet_xml)
        self.assertIn("2026-06-18", sheet_xml)
        self.assertIn("11:17:29", sheet_xml)

    def test_generates_behave_report_with_test_cases_and_stages(self):
        result = {
            "run_id": "20260702_170924",
            "case_name": "Run migrated happy path from Behave",
            "status": "PASSED",
            "started_at": "2026-07-02T17:09:24",
            "test_cases": [
                {
                    "id": "TC01",
                    "name": "normal_magna_1250",
                    "status": "PASSED",
                    "started_at": "2026-07-02T17:10:00",
                    "stages": [
                        {
                            "name": "00_prepare_product_selection",
                            "status": "PASSED",
                        },
                        {
                            "name": "05_windows_app_and_finalize",
                            "status": "PASSED",
                        },
                    ],
                },
                {
                    "id": "TC02",
                    "name": "normal_premium_500",
                    "status": "PASSED",
                    "started_at": "2026-07-02T17:12:00",
                    "stages": [
                        {
                            "name": "00_prepare_product_selection",
                            "status": "PASSED",
                        }
                    ],
                },
            ],
        }

        with tempfile.TemporaryDirectory() as temp_directory:
            report_path = generate_excel_report(
                result,
                Path(temp_directory),
                "20260702_170924",
            )

            with ZipFile(report_path) as workbook:
                sheet_xml = workbook.read(
                    "xl/worksheets/sheet1.xml"
                ).decode("utf-8")

        self.assertIn("TC01", sheet_xml)
        self.assertIn("TC02", sheet_xml)
        self.assertIn("normal_magna_1250", sheet_xml)
        self.assertIn("00_prepare_product_selection", sheet_xml)
        self.assertIn("Stage ejecutado correctamente.", sheet_xml)


if __name__ == "__main__":
    unittest.main()
