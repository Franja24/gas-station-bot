@print
Feature: Print flow

  Scenario: Run print from Behave
    Given the automation workspace is ready
    When I run the "print" flow
    Then the "print" flow should finish
