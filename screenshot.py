from datetime import datetime
from pathlib import Path

import pyautogui

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet


RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")

RUN_FOLDER = Path(f"evidencias/run_{RUN_ID}")

SCREENSHOTS_FOLDER = RUN_FOLDER / "screenshots"

SCREENSHOTS_FOLDER.mkdir(parents=True, exist_ok=True)


def save_screenshot(name):

    filename = SCREENSHOTS_FOLDER / f"{name}.png"

    screenshot = pyautogui.screenshot()

    screenshot.save(str(filename))

    print(f"[OK] Screenshot guardado: {filename.resolve()}")
    print(f"[DEBUG] Existe?: {filename.exists()}")


def generate_pdf_report():

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

    print(f"[OK] PDF generado: {pdf_path}")