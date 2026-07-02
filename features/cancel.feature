@cancel
Feature: Cancel flow

  Scenario: Run cancel from Behave
    Given the automation workspace is ready
    When I run the "cancel" flow
    Then the "cancel" flow should finish
