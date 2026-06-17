@login
Feature: Login flow

  Scenario: Run login from Behave
    Given the automation workspace is ready
    When I run the "login" flow
    Then the "login" flow should finish
