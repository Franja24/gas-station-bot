from case_runner import run_stages
from detector import find_image
from features.active_session_start import run as active_session_start_run
from features.magna_amount_200 import run as magna_amount_200_run
from features.open_kiosco import run as open_kiosco_run
from features.print_ticket import run as print_ticket_run
from features.windows_app import run as windows_run


def _tdc_stages(include_open_kiosco=True):
    stages = []

    if include_open_kiosco:
        stages.append(("00_open_kiosco", open_kiosco_run))

    stage_offset = len(stages)
    stages.extend(
        [
            (
                f"{stage_offset + 0:02d}_active_session_start",
                active_session_start_run,
            ),
            (f"{stage_offset + 1:02d}_magna_amount_200", magna_amount_200_run),
            (f"{stage_offset + 2:02d}_windows", windows_run),
            (f"{stage_offset + 3:02d}_print_ticket", print_ticket_run),
        ]
    )

    return stages


def run():
    return run_stages(_tdc_stages(include_open_kiosco=True))


def _is_visible(image_name, confidence=0.80, timeout=1):
    return find_image(image_name, confidence=confidence, timeout=timeout) is not None


def run_from_start_screen():
    if _is_visible("payment_success.png", timeout=2):
        print("[TDC CURRENT] Pago exitoso ya visible; continuando con despacho")
        return run_stages(
            [
                ("00_windows", windows_run),
                ("01_print_ticket", print_ticket_run),
            ]
        )

    if (
        _is_visible("premium.png", timeout=1)
        and _is_visible("magna.png", timeout=1)
    ):
        print("[TDC CURRENT] Seleccion de combustible ya visible")
        return run_stages(
            [
                ("00_magna_amount_200", magna_amount_200_run),
                ("01_windows", windows_run),
                ("02_print_ticket", print_ticket_run),
            ]
        )

    return run_stages(_tdc_stages(include_open_kiosco=False))
