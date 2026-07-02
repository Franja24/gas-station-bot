@benefits
Feature: Benefits flow

  Scenario: Run benefits from Behave
    Given the automation workspace is ready
    When I run the "benefits" flow
    Then the "benefits" flow should finish
