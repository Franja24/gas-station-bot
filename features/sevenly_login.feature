@sevenly_login
Feature: Sevenly login flow

  Scenario: Run Sevenly phone login from Behave
    Given the automation workspace is ready
    When I run the "sevenly_login" flow
    Then the "sevenly_login" flow should finish
