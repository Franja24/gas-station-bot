@lt_e2e
Feature: Liters e2e flow

  Scenario: Run liters e2e from Behave
    Given the automation workspace is ready
    When I run the "lt_e2e" flow
    Then the "lt_e2e" flow should finish
