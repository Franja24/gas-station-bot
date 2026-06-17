from config.local_coordinates import load_local_coordinates


DEFAULT_COORDINATES = {
    "start.png": (700, 520),
    "petro_kiosk_app_icon": (429, 19),
    "login_button.png": (680, 535),
    "entry_button.png": (650, 500),
    "activate_unit.png": (680, 530),
    "sevenly.png": (718, 123),
    "premium.png": (640, 256),
    "magna.png": (640, 398),
    "amount_1250.png": (752, 300),
    "amount_500_premium.png": (835, 360),
    "no_benefits_button.png": (650, 450),
    "continue_button.png": (800, 530),
    "card.png": (650, 420),
    "print.png": (700, 460),
    "invoice.png": (800, 340),
    "benefits_telefon_number_button.png": (700, 385),
    "telefon_number.png": (700, 385),
    "charge_type_amount_tab.png": (625, 183),
    "charge_amount_500.png": (752, 263),
    "charge_type_liters_tab.png": (683, 183),
    "charge_liters_20.png": (752, 263),
    "finalize_button.png": (770, 520),
    "invoice_continue_button.png": (770, 520),
    "print_continue_button.png": (770, 520),
}


COORDINATES = load_local_coordinates("coordinates", DEFAULT_COORDINATES)
