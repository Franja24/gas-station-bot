@sevenly_login_error
Feature: Sevenly login error flow

  Scenario: Run Sevenly login error from Behave
    Given the automation workspace is ready
    When I run the "sevenly_login_error" flow
    Then the "sevenly_login_error" flow should finish
