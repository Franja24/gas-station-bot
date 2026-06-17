@premium
Feature: Premium flow

  Scenario: Run premium purchase from Behave
    Given the automation workspace is ready
    When I run the "premium" flow
    Then the "premium" flow should finish
