@login_error
Feature: Login error flow

  Scenario: Invalid login shows an error
    Given the automation workspace is ready
    When I run the "login_error" flow
    Then the "login_error" flow should finish
