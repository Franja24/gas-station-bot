@cancel_e2e
Feature: Cancel e2e flow

  Scenario: Run cancel e2e from Behave
    Given the automation workspace is ready
    When I run the "cancel_e2e" flow
    Then the "cancel_e2e" flow should finish
