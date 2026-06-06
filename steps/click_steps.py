from behave import given, when, then

from clicker import click_image
from screenshot import save_screenshot


@given("the application is ready")
def step_ready(context):
    print("Application ready")


@when('we click on the "{button}" button')
def step_click_button(context, button):

    image_map = {
        "magna": "magna.png",
        "premium": "premium.png",
        "amount_1250": "amount_1250.png",
        "amount_500_premium": "amount_500_premium.png",
        "continue": "continue_button.png",
        "no_benefits": "no_benefits_button.png",
        "card": "card.png",
    }

    click_image(image_map[button], timeout=10)

    save_screenshot(button)


@then("the happy path should be completed")
def step_completed(context):
    print("Happy Path Completed")
