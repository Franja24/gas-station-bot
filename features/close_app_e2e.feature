@close_app_e2e
Feature: Close app e2e flow

  Scenario: Run close app e2e from Behave
    Given the automation workspace is ready
    When I run the "close_app_e2e" flow
    Then the "close_app_e2e" flow should finish
