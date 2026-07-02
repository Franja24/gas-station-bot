@premium_close_app
Feature: Premium close app flow

  Scenario: Run premium close app from Behave
    Given the automation workspace is ready
    When I run the "premium_close_app" flow
    Then the "premium_close_app" flow should finish
