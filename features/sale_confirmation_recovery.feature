@sale_confirmation_recovery
Feature: Sale confirmation recovery flow

  Scenario: Recover sale confirmation from Behave
    Given the automation workspace is ready
    When I run the "sale_confirmation_recovery" flow
    Then the "sale_confirmation_recovery" flow should finish
