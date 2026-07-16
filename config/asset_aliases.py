from features.platform_profile import get_automation_platform


WINDOWS_ALIASES = {
    "login_button.png": ["login_button_windows.png", "login_button.png"],
    "login_form_anchor.png": [
        "login_form_anchor_windows.png",
        "login_form_anchor.png",
    ],
    "entry_button.png": ["entry_button_windows.png", "entry_button.png"],
    "login_error.png": ["login_error_windows.png", "login_error.png"],
    "user_field.png": ["user_field_windows.png", "user_field.png"],
    "pass_field.png": ["pass_field_windows.png", "pass_field.png"],
    "login_zero_button.png": [
        "login_zero_button_windows.png",
        "login_zero_button.png",
    ],
    "login_one_button.png": [
        "login_one_button_windows.png",
        "login_one_button.png",
    ],
    "login_two_button.png": [
        "login_two_button_windows.png",
        "login_two_button.png",
    ],
    "login_three_button.png": [
        "login_three_button_windows.png",
        "login_three_button.png",
    ],
    "login_four_button.png": [
        "login_four_button_windows.png",
        "login_four_button.png",
    ],
    "login_five_button.png": [
        "login_five_button_windows.png",
        "login_five_button.png",
    ],
    "login_six_button.png": [
        "login_six_button_windows.png",
        "login_six_button.png",
    ],
    "login_seven_button.png": [
        "login_seven_button_windows.png",
        "login_seven_button.png",
    ],
    "login_eight_button.png": [
        "login_eight_button_windows.png",
        "login_eight_button.png",
    ],
    "login_nine_button.png": [
        "login_nine_button_windows.png",
        "login_nine_button.png",
    ],
    "continue_button.png": [
        "continue_button.png",
        "continue_amount_button.png",
    ],
    "start.png": ["start.png"],
    "iniciar.png": ["start.png"],
}


def get_image_candidates(image_name):
    platform_name = get_automation_platform()

    if platform_name == "windows":
        candidates = WINDOWS_ALIASES.get(image_name, [image_name])
    else:
        if image_name == "start.png":
            candidates = ["start.png", "iniciar.png"]
        elif image_name == "iniciar.png":
            candidates = ["iniciar.png", "start.png"]
        else:
            candidates = [image_name]

    ordered_candidates = []
    seen = set()

    for candidate in candidates:
        if candidate in seen:
            continue

        seen.add(candidate)
        ordered_candidates.append(candidate)

    return ordered_candidates
