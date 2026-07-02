@sevenly_e2e
Feature: Sevenly e2e flow

  Scenario: Run Sevenly e2e from Behave
    Given the automation workspace is ready
    When I run the "sevenly_e2e" flow
    Then the "sevenly_e2e" flow should finish
