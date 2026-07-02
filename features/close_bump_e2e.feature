@close_bump_e2e
Feature: Close bump e2e flow

  Scenario: Run close bump e2e from Behave
    Given the automation workspace is ready
    When I run the "close_bump_e2e" flow
    Then the "close_bump_e2e" flow should finish
