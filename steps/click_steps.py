from behave import given, when, then

import time

from clicker import assert_image_visible, click_image
from screenshot import save_screenshot


DIGITS = {
    "0": "zero_button.png",
    "1": "one_button.png",
    "2": "two_button.png",
    "3": "three_button.png",
    "4": "four_button.png",
    "5": "five_button.png",
    "6": "six_button.png",
    "7": "seven_button.png",
    "8": "eight_button.png",
    "9": "nine_button.png",
}


@given("the application is ready")
def step_ready(context):
    print("Application ready")


@when('we click on the "{button}" button')
def step_click_button(context, button):

    image_map = {
        "magna": "magna.png",
        "premium": "premium.png",
        "sevenly": "sevenly.png",
        "telefon_number": "telefon_number.png",
        "amount_1250": "amount_1250.png",
        "amount_500_premium": "amount_500_premium.png",
        "continue": "continue_button.png",
        "no_benefits": "no_benefits_button.png",
        "card": "card.png",
    }

    click_image(image_map[button], timeout=10)

    save_screenshot(button)


@when('we enter phone number "{phone_number}"')
def step_enter_phone_number(context, phone_number):
    for digit in phone_number:
        click_image(DIGITS[digit], timeout=10)

        time.sleep(2)

    save_screenshot("phone_number_entered")


@then("the happy path should be completed")
def step_completed(context):
    print("Happy Path Completed")


@then('the "{message}" error message should be displayed')
def step_error_message_displayed(context, message):
    assert_image_visible(f"{message}.png", confidence=0.80, timeout=15)

    save_screenshot(f"{message}_visible")
