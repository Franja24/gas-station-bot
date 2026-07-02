@e2e
Feature: E2e flow

  Scenario: Run e2e from Behave
    Given the automation workspace is ready
    When I run the "e2e" flow
    Then the "e2e" flow should finish
