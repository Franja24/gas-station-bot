@close_app_dispensing_recovery
Feature: Close app dispensing recovery flow

  Scenario: Close app while dispensing from start screen
    Given the automation workspace is ready
    When I run the "close_app_dispensing_recovery" flow
    Then the "close_app_dispensing_recovery" flow should finish
