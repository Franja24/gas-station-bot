@magna
Feature: Magna flow

  Scenario: Run Magna purchase from Behave
    Given the automation workspace is ready
    When I run the "magna" flow
    Then the "magna" flow should finish
