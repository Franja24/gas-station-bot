from importlib import import_module
import os

from behave import given, then, when


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


def run_flow(context, flow_name):
    normalized_flow = normalize_flow_name(flow_name)

    if normalized_flow not in FLOW_RUNNERS:
        available_flows = ", ".join(sorted(FLOW_RUNNERS))
        raise ValueError(
            f"Flujo no soportado: {flow_name}. "
            f"Disponibles: {available_flows}"
        )

    print(f"[BEHAVE] Ejecutando flujo: {normalized_flow}")
    try:
        returned_details = FLOW_RUNNERS[normalized_flow]()
    except Exception as exc:
        if hasattr(exc, "stages"):
            context.behave_stages.extend(exc.stages)
        context.behave_error = f"{type(exc).__name__}: {exc}"
        raise

    if isinstance(returned_details, dict):
        context.behave_stages.extend(returned_details.get("stages", []))

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
    for row in context.table:
        normalized_flow = normalize_flow_name(row["flow"])
        context.expected_flows.append(normalized_flow)
        context.completed_flows.append(run_flow(context, normalized_flow))


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
