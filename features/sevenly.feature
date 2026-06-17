@sevenly
Feature: Sevenly full flow

  Scenario: Run full Sevenly path from Behave
    Given the automation workspace is ready
    When I run the "sevenly" flow
    Then the "sevenly" flow should finish
