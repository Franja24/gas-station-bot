from behave import given, then, when


def run_login():
    from features.login import run

    run()


def run_login_error():
    from features.login_error import run

    run()


def run_magna():
    from features.magna import run

    run()


def run_open_kiosco():
    from features.open_kiosco import run

    run()


def run_premium():
    from features.premium import run

    run()


def run_sevenly_login():
    from features.sevenly_login import run

    run()


def run_invoice():
    from features.invoice import run

    run(submit_print=False)


def run_invoice_full():
    from features.invoice import run

    run(submit_print=True)


def run_print():
    from features.print import run

    run()


def run_windows_app():
    from features.windows_app import run

    run()


def run_windows_app_close():
    from features.windows_app_close import run

    run()


def run_sevenly():
    from features.sevenly import run

    run()


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
    "login": run_login,
    "login error": run_login_error,
    "login_error": run_login_error,
    "magna": run_magna,
    "open kiosco": run_open_kiosco,
    "open_kiosco": run_open_kiosco,
    "premium": run_premium,
    "sevenly login": run_sevenly_login,
    "sevenly_login": run_sevenly_login,
    "sevenly": run_sevenly,
    "invoice": run_invoice,
    "invoice_full": run_invoice_full,
    "print": run_print,
    "windows app": run_windows_app,
    "windows_app": run_windows_app,
    "windows app close": run_windows_app_close,
    "windows_app_close": run_windows_app_close,
    "windows_app_clos": run_windows_app_close,
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
    FLOW_RUNNERS[normalized_flow]()
    context.last_flow = normalized_flow
    return normalized_flow


@given("the automation workspace is ready")
def step_workspace_ready(context):
    context.last_flow = None
    context.completed_flows = []
    print("[BEHAVE] Workspace listo")


@when('I run the "{flow_name}" flow')
def step_run_flow(context, flow_name):
    run_flow(context, flow_name)


@when("I run these flows")
def step_run_flows(context):
    if context.table is None:
        raise ValueError("Agrega una tabla Behave con la columna 'flow'")

    for row in context.table:
        context.completed_flows.append(run_flow(context, row["flow"]))


@when("I run the happy path")
def step_run_happy_path(context):
    for flow_name in HAPPY_PATH_FLOWS:
        context.completed_flows.append(run_flow(context, flow_name))
    context.last_flow = "happy_path"


@then('the "{flow_name}" flow should finish')
def step_flow_finished(context, flow_name):
    normalized_flow = normalize_flow_name(flow_name)
    assert context.last_flow == normalized_flow
    print(f"[BEHAVE] Flujo terminado: {normalized_flow}")


@then("the happy path should finish")
def step_happy_path_finished(context):
    assert context.completed_flows == HAPPY_PATH_FLOWS
    print("[BEHAVE] Happy path terminado")
