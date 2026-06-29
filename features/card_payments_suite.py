from case_runner import run_suite
from features.tdc_from_active_session import run as tdc_from_active_session_run
from features.tdd_e2e import run as tdd_e2e_run


def run():
    return run_suite(
        [
            ("01_tdd_e2e", tdd_e2e_run),
            ("02_tdc_from_active_session", tdc_from_active_session_run),
        ]
    )
