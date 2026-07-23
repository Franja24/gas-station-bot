from case_runner import run_stages
from clicker import assert_image_visible, click_image
from features.applications import open_anydesk
from screenshot import save_screenshot


EMPLOYEE_SEQUENCE = ("7", "6", "5", "8")
HUMAN_CARD_TIMEOUT_SECONDS = 10


def click_asset(image_name, timeout=10):
    return click_image(
        image_name,
        timeout=timeout,
        use_coordinates=False,
        use_region=False,
    )


def _focus_product_selection():
    open_anydesk()
    save_screenshot("employee_change_product_selection_ready")


def _wait_for_employee_card(employee_number):
    print(
        "[BOT_HUMANO] Presenta la tarjeta para cambiar al "
        f"Empleado {employee_number}."
    )
    assert_image_visible(
        "change_employee_activate_button.png",
        confidence=0.80,
        timeout=HUMAN_CARD_TIMEOUT_SECONDS,
    )
    save_screenshot(f"employee_{employee_number}_change_screen")


def _activate_employee(employee_number):
    click_asset("change_employee_activate_button.png", timeout=10)
    assert_image_visible(
        "activate_unit_button.png",
        confidence=0.80,
        timeout=15,
    )
    save_screenshot(f"employee_{employee_number}_welcome_screen")


def _activate_unit(employee_number):
    click_asset("activate_unit_button.png", timeout=10)
    assert_image_visible("start.png", confidence=0.80, timeout=15)
    save_screenshot(f"employee_{employee_number}_start_ready")


def run(iterations=4):
    employees = EMPLOYEE_SEQUENCE[:iterations]
    if len(employees) != iterations:
        raise ValueError(
            f"Solo hay {len(EMPLOYEE_SEQUENCE)} empleados configurados "
            "para CP_AV_007."
        )

    stages = [("00_focus_product_selection", _focus_product_selection)]
    for index, employee_number in enumerate(employees, start=1):
        stages.extend(
            [
                (
                    f"{index:02d}_wait_card_employee_{employee_number}",
                    lambda number=employee_number: _wait_for_employee_card(number),
                ),
                (
                    f"{index:02d}_activate_employee_{employee_number}",
                    lambda number=employee_number: _activate_employee(number),
                ),
                (
                    f"{index:02d}_activate_unit_employee_{employee_number}",
                    lambda number=employee_number: _activate_unit(number),
                ),
            ]
        )

    return run_stages(stages)
