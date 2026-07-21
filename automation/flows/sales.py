from features.magna_amount_payment import run_amount_payment


def start_amount_sale(
    product,
    amount,
    *,
    require_payment_approval=False,
):
    product = product.strip().lower()
    amount = str(amount)
    evidence_slug = f"{product}_amount_{amount}"

    return run_amount_payment(
        amount,
        evidence_slug,
        product=product,
        require_payment_approval=require_payment_approval,
    )
