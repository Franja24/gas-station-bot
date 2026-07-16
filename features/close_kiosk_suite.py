from case_runner import run_suite
from features.cleanup_after_fueling import run as cleanup_after_fueling_run
from features.cleanup_after_hose_unhooked import (
    run as cleanup_after_hose_unhooked_run,
)
from features.close_at_payment_screen_e2e import (
    run as close_at_payment_screen_e2e_run,
)
from features.close_while_fueling_from_product_selection_e2e import (
    run as close_while_fueling_run,
)
from features.close_with_hose_unhooked_from_product_selection_e2e import (
    run as close_with_hose_unhooked_e2e_run,
)


def run():
    return run_suite(
        [
            ("01_close_at_payment_screen", close_at_payment_screen_e2e_run),
            ("02_close_with_hose_unhooked", close_with_hose_unhooked_e2e_run),
            (
                "02_5_cleanup_after_hose_unhooked",
                cleanup_after_hose_unhooked_run,
                {"reportable": False, "kind": "cleanup"},
            ),
            ("03_close_while_fueling_and_confirm", close_while_fueling_run),
            (
                "03_5_cleanup_after_fueling",
                cleanup_after_fueling_run,
                {"reportable": False, "kind": "cleanup"},
            ),
        ]
    )
