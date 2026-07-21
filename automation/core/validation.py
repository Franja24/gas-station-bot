from clicker import assert_image_visible


def employee_login_is_visible():
    assert_image_visible("login_button.png", confidence=0.80, timeout=15)


def require_approved_payment(result, sale_label):
    if result != "approved":
        raise AssertionError(
            f"Expected approved payment for {sale_label}, received: {result}"
        )
