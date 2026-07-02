@login_error
Feature: Login error flow

  Scenario: Run login error from Behave
    Given the automation workspace is ready
    When I run the "login_error" flow
    Then the "login_error" flow should finish
