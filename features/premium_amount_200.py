from features.magna_amount_payment import run_amount_payment


LAST_PAYMENT_RESULT = None


def get_last_payment_result():
    return LAST_PAYMENT_RESULT


def run():
    global LAST_PAYMENT_RESULT

    LAST_PAYMENT_RESULT = run_amount_payment(
        "200",
        "premium_amount_200",
        product="premium",
        require_payment_approval=True,
    )
    return LAST_PAYMENT_RESULT
