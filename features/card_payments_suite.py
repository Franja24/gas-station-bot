from case_runner import run_suite
from features.tdc_e2e import run as tdc_e2e_run
from features.tdd_e2e import run as tdd_e2e_run


def run():
    return run_suite(
        [
            ("01_tdd_e2e", tdd_e2e_run),
            ("02_tdc_e2e", tdc_e2e_run),
        ]
    )
