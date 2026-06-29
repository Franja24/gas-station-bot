from case_runner import run_suite
from features.print_e2e import run as print_e2e_100_run
from features.print_e2e_150 import run as print_e2e_150_run


def run():
    return run_suite(
        [
            ("01_print_e2e_100", print_e2e_100_run),
            ("02_print_e2e_150", print_e2e_150_run),
        ]
    )
