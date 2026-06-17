from behave import given, then, when


def run_login():
    from features.login import run

    run()


def run_login_error():
    from features.login_error import run

    run()


def run_premium():
    from features.premium import run

    run()


def run_invoice():
    from features.invoice import run

    run()


def run_windows_app():
    from features.windows_app import run

    run()


def run_sevenly():
    from features.sevenly import run

    run()


FLOW_RUNNERS = {
    "login": run_login,
    "login error": run_login_error,
    "login_error": run_login_error,
    "premium": run_premium,
    "sevenly": run_sevenly,
    "invoice": run_invoice,
    "windows app": run_windows_app,
    "windows_app": run_windows_app,
}


@given("the automation workspace is ready")
def step_workspace_ready(context):
    context.last_flow = None
    print("[BEHAVE] Workspace listo")


@when('I run the "{flow_name}" flow')
def step_run_flow(context, flow_name):
    normalized_flow = flow_name.strip().lower()

    if normalized_flow not in FLOW_RUNNERS:
        available_flows = ", ".join(sorted(FLOW_RUNNERS))
        raise ValueError(
            f"Flujo no soportado: {flow_name}. "
            f"Disponibles: {available_flows}"
        )

    print(f"[BEHAVE] Ejecutando flujo: {normalized_flow}")
    FLOW_RUNNERS[normalized_flow]()
    context.last_flow = normalized_flow


@then('the "{flow_name}" flow should finish')
def step_flow_finished(context, flow_name):
    normalized_flow = flow_name.strip().lower()
    assert context.last_flow == normalized_flow
    print(f"[BEHAVE] Flujo terminado: {normalized_flow}")
