from importlib import import_module
import os
import time
from datetime import datetime

from behave import given, then, when
import screenshot


def module_runner(module_name, **kwargs):
    def run_module():
        module = import_module(f"features.{module_name}")
        return module.run(**kwargs)

    return run_module


def asset_filename(asset_name):
    if asset_name.endswith(".png"):
        return asset_name

    return f"{asset_name}.png"


HAPPY_PATH_FLOWS = [
    "open_kiosco",
    "login",
    "magna",
    "premium",
    "sevenly_login",
    "windows_app",
    "windows_app_close",
    "invoice",
    "print",
]


FLOW_RUNNERS = {
    "benefits": module_runner("benefits"),
    "cancel": module_runner("cancel"),
    "cancel_e2e": module_runner("cancel_e2e"),
    "change type charge": module_runner("change_type_charge"),
    "change_type_charge": module_runner("change_type_charge"),
    "normal_magna_1250": module_runner(
        "charge_operation",
        product="magna",
        charge_type="amount_1250",
    ),
    "normal_premium_500": module_runner(
        "charge_operation",
        product="premium",
        charge_type="amount_500",
    ),
    "sevenly_magna_liters_20": module_runner(
        "charge_operation",
        product="magna",
        charge_type="liters_20",
        use_sevenly=True,
    ),
    "close_app_dispensing_recovery": module_runner("close_app_dispensing_recovery"),
    "close_app_e2e": module_runner("close_app_e2e"),
    "close_bump_e2e": module_runner("close_bump_e2e"),
    "declined_transaction_e2e": module_runner("declined_transaction_e2e"),
    "declined_transaction_request": module_runner("declined_transaction_request"),
    "e2e": module_runner("e2e"),
    "invoice": module_runner("invoice", submit_print=False),
    "invoice_full": module_runner("invoice", submit_print=True),
    "kios_011": module_runner("change_type_charge"),
    "login": module_runner("login"),
    "login error": module_runner("login_error"),
    "login_error": module_runner("login_error"),
    "lt_e2e": module_runner("lt_e2e"),
    "magna": module_runner("magna"),
    "normal_magna_continue": module_runner("normal_magna_continue"),
    "normal_magna": module_runner("normal_magna"),
    "open kiosco": module_runner("open_kiosco"),
    "open_kiosco": module_runner("open_kiosco"),
    "premium": module_runner("premium"),
    "premium_close_app": module_runner("premium_close_app"),
    "print": module_runner("print"),
    "sevenly": module_runner("sevenly"),
    "sevenly_e2e": module_runner("sevenly_e2e"),
    "sevenly login": module_runner("sevenly_login"),
    "sevenly_login": module_runner("sevenly_login"),
    "sevenly_login_error": module_runner("sevenly_login_error"),
    "sale_confirmation_recovery": module_runner("sale_confirmation_recovery"),
    "transaction_cancel_recovery": module_runner("transaction_cancel_recovery"),
    "unhook_hose_before_payment_approval": module_runner(
        "unhook_hose_before_payment_approval_e2e"
    ),
    "windows": module_runner("windows_app"),
    "windows app": module_runner("windows_app"),
    "windows_app": module_runner("windows_app"),
    "windows app close": module_runner("windows_app_close"),
    "windows_app_close": module_runner("windows_app_close"),
    "windows_app_clos": module_runner("windows_app_close"),
    "windows_app_close_hung_up": module_runner("windows_app_close_hung_up"),
    "windows_app_hang_up": module_runner("windows_app_hang_up"),
}


def normalize_flow_name(flow_name):
    normalized_flow = flow_name.strip().lower()
    normalized_flow = normalized_flow.replace(" _", "_").replace("_ ", "_")
    return " ".join(normalized_flow.split())


def table_value(row, column_name, default=None):
    try:
        value = row[column_name]
    except (KeyError, IndexError, TypeError):
        if hasattr(row, "get"):
            value = row.get(column_name, default)
        else:
            value = default

    if value is None:
        return default

    value = str(value).strip()
    return value if value else default


def _append_behave_case(
    context,
    case_id,
    flow_name,
    started_at,
    start_time,
    status,
    stages,
    error=None,
    case_name=None,
):
    if not hasattr(context, "behave_test_cases"):
        context.behave_test_cases = []

    context.behave_test_cases.append(
        {
            "id": case_id,
            "name": case_name or flow_name,
            "flow": flow_name,
            "status": status,
            "started_at": started_at.isoformat(timespec="seconds"),
            "duration_seconds": round(time.monotonic() - start_time, 2),
            "error": error,
            "stages": stages,
        }
    )


def run_flow(context, flow_name, case_id=None, case_name=None):
    normalized_flow = normalize_flow_name(flow_name)

    if normalized_flow not in FLOW_RUNNERS:
        available_flows = ", ".join(sorted(FLOW_RUNNERS))
        raise ValueError(
            f"Flujo no soportado: {flow_name}. "
            f"Disponibles: {available_flows}"
        )

    started_at = datetime.now()
    start_time = time.monotonic()
    screenshot_case = f"{case_id}_{normalized_flow}" if case_id else None

    if screenshot_case:
        screenshot.set_screenshot_case(screenshot_case)

    print(f"[BEHAVE] Ejecutando flujo: {normalized_flow}")
    try:
        returned_details = FLOW_RUNNERS[normalized_flow]()
    except Exception as exc:
        stages = []
        if hasattr(exc, "stages"):
            stages = exc.stages
            context.behave_stages.extend(stages)
        if case_id:
            _append_behave_case(
                context,
                case_id,
                normalized_flow,
                started_at,
                start_time,
                "FAILED",
                stages,
                f"{type(exc).__name__}: {exc}",
                case_name,
            )
        context.behave_error = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        if screenshot_case:
            screenshot.set_screenshot_case(None)

    if isinstance(returned_details, dict):
        stages = returned_details.get("stages", [])
        context.behave_stages.extend(stages)
        if case_id:
            _append_behave_case(
                context,
                case_id,
                normalized_flow,
                started_at,
                start_time,
                "PASSED",
                stages,
                case_name=case_name,
            )
    else:
        stages = []
        if case_id:
            _append_behave_case(
                context,
                case_id,
                normalized_flow,
                started_at,
                start_time,
                "PASSED",
                stages,
                case_name=case_name,
            )

    context.last_flow = normalized_flow
    return normalized_flow


@given("the automation workspace is ready")
def step_workspace_ready(context):
    if not hasattr(context, "remote_desktop_app"):
        from features.applications import REMOTE_DESKTOP_APP_ENV, use_remote_desktop

        use_remote_desktop(os.environ.get(REMOTE_DESKTOP_APP_ENV, "AnyDesk"))

    context.last_flow = None
    context.completed_flows = []
    context.expected_flows = []
    context.behave_test_cases = []
    context.behave_background_stages = []
    print("[BEHAVE] Workspace listo")


@given('the remote desktop app is "{app_name}"')
def step_remote_desktop_app(context, app_name):
    from features.applications import use_remote_desktop

    use_remote_desktop(app_name)
    context.remote_desktop_app = app_name


@when('I run the "{flow_name}" flow')
def step_run_flow(context, flow_name):
    run_flow(context, flow_name)


@when("I run these flows")
def step_run_flows(context):
    if context.table is None:
        raise ValueError("Agrega una tabla Behave con la columna 'flow'")

    context.expected_flows = []
    context.behave_background_stages = list(
        getattr(context, "behave_stages", [])
    )
    for index, row in enumerate(context.table, start=1):
        case_id = table_value(row, "case_id", f"TC{index:02d}")
        checkpoint = table_value(row, "checkpoint")
        flow_name = table_value(row, "flow")
        if not flow_name:
            raise ValueError("Agrega una tabla Behave con la columna 'flow'")

        normalized_flow = normalize_flow_name(flow_name)
        context.expected_flows.append(normalized_flow)
        context.completed_flows.append(
            run_flow(
                context,
                normalized_flow,
                case_id=case_id,
                case_name=checkpoint,
            )
        )


@when("I register these assisted checkpoints")
def step_register_assisted_checkpoints(context):
    if context.table is None:
        raise ValueError("Agrega una tabla Behave con la columna 'case_id'")

    context.expected_assisted_checkpoints = []

    for index, row in enumerate(context.table, start=1):
        case_id = table_value(row, "case_id", f"BOT_HUMANO_{index:02d}")
        checkpoint = table_value(row, "checkpoint", case_id)
        bot_scope = table_value(row, "bot_scope", "Evidencia visual y navegación")
        human_scope = table_value(row, "human_scope", "Validación humana requerida")
        started_at = datetime.now()

        context.expected_assisted_checkpoints.append(case_id)
        if not hasattr(context, "behave_test_cases"):
            context.behave_test_cases = []

        context.behave_test_cases.append(
            {
                "id": case_id,
                "name": checkpoint,
                "flow": "bot_humano",
                "status": "ASSISTED",
                "started_at": started_at.isoformat(timespec="seconds"),
                "duration_seconds": 0,
                "error": None,
                "stages": [
                    {
                        "name": "bot_scope",
                        "status": "ASSISTED",
                        "started_at": started_at.isoformat(timespec="seconds"),
                        "duration_seconds": 0,
                        "error": bot_scope,
                    },
                    {
                        "name": "human_scope",
                        "status": "PENDING_HUMAN",
                        "started_at": started_at.isoformat(timespec="seconds"),
                        "duration_seconds": 0,
                        "error": human_scope,
                    },
                ],
            }
        )


@when("I run the happy path")
def step_run_happy_path(context):
    for flow_name in HAPPY_PATH_FLOWS:
        context.completed_flows.append(run_flow(context, flow_name))
    context.last_flow = "happy_path"


@then('the "{asset_name}" asset should be visible')
def step_asset_should_be_visible(context, asset_name):
    from clicker import assert_image_visible

    image_name = asset_filename(asset_name)
    assert_image_visible(image_name, confidence=0.80, timeout=30)


@then('the "{flow_name}" flow should finish')
def step_flow_finished(context, flow_name):
    normalized_flow = normalize_flow_name(flow_name)
    assert context.last_flow == normalized_flow
    print(f"[BEHAVE] Flujo terminado: {normalized_flow}")


@then("the happy path should finish")
def step_happy_path_finished(context):
    assert context.completed_flows == HAPPY_PATH_FLOWS
    print("[BEHAVE] Happy path terminado")


@then("the selected flows should finish")
def step_selected_flows_finished(context):
    if not context.expected_flows:
        raise AssertionError("No hay flujos seleccionados para validar")

    assert context.completed_flows == context.expected_flows
    print(f"[BEHAVE] Flujos terminados: {', '.join(context.completed_flows)}")


@then("the assisted checkpoints should be documented")
def step_assisted_checkpoints_documented(context):
    expected = getattr(context, "expected_assisted_checkpoints", [])
    if not expected:
        raise AssertionError("No hay checkpoints asistidos para validar")

    documented = [
        case["id"]
        for case in getattr(context, "behave_test_cases", [])
        if case.get("status") == "ASSISTED"
    ]

    assert documented == expected
    print(f"[BEHAVE] Checkpoints asistidos documentados: {', '.join(documented)}")
