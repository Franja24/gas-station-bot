from clicker import ClickError, click_image


def click_transaction(expected_amount=None, timeout=5):
    if expected_amount is not None:
        amount_asset = f"transaction_amount_{expected_amount}.png"

        try:
            click_image(
                amount_asset,
                timeout=timeout,
                use_coordinates=False,
                use_region=False,
            )
            print(
                f"[TRANSACTION LOG] Transacción de ${expected_amount} "
                "seleccionada por monto."
            )
            return
        except (ClickError, FileNotFoundError) as exc:
            print(
                f"[TRANSACTION LOG] Asset {amount_asset} no disponible: {exc}. "
                "Usando la primera transacción como respaldo."
            )

    click_image(
        "transaction_log_first_row_marker.png",
        timeout=10,
        use_coordinates=False,
        use_region=False,
    )
