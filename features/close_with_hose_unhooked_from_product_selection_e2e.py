from case_runner import run_stages
from features.activate_unit_for_out_of_service import (
    run as activate_unit_for_out_of_service_run,
)
from features.login_if_needed import run as login_if_needed_run
from features.magna_amount_150_approved import (
    get_last_payment_result,
    run as magna_amount_150_approved_run,
)
from features.open_kiosco_ready import run as open_kiosco_ready_run
from features.validate_out_of_service import run as validate_out_of_service_run
from features.windows_app_unhook_close import run as windows_app_unhook_close_run


def run_if_payment_approved(stage_function, stage_name):
    if get_last_payment_result() == "declined":
        print(f"[PAYMENT ROUTE] Omitiendo {stage_name}: pago declinado")
        return

    return stage_function()


def unhook_close_if_approved():
    return run_if_payment_approved(
        windows_app_unhook_close_run,
        "descolgar y cerrar kiosco",
    )


def open_kiosk_if_approved():
    return run_if_payment_approved(open_kiosco_ready_run, "abrir kiosco")


def activate_unit_if_approved():
    return run_if_payment_approved(
        activate_unit_for_out_of_service_run,
        "activar unidad",
    )


def validate_out_of_service_if_approved():
    return run_if_payment_approved(
        validate_out_of_service_run,
        "validar bomba fuera de servicio",
    )


def run():
    return run_stages(
        [
            ("01_login_if_needed", login_if_needed_run),
            (
                "02_magna_amount_150_wait_for_payment_approval",
                magna_amount_150_approved_run,
            ),
            ("03_windows_app_unhook_close", unhook_close_if_approved),
            ("04_open_kiosco", open_kiosk_if_approved),
            (
                "05_activate_unit_for_out_of_service",
                activate_unit_if_approved,
            ),
            ("06_validate_out_of_service", validate_out_of_service_if_approved),
        ]
    )
