from features.magna_amount_payment import run_amount_payment


LAST_PAYMENT_RESULT = None


def run():
    global LAST_PAYMENT_RESULT

    LAST_PAYMENT_RESULT = run_amount_payment(
        "150",
        "magna_amount_150_approved",
        require_payment_approval=True,
    )
    return LAST_PAYMENT_RESULT


def get_last_payment_result():
    return LAST_PAYMENT_RESULT
