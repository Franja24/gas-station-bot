@windows_app_close_hung_up
Feature: Windows app close hung up flow

  Scenario: Run Windows app close hung up from Behave
    Given the automation workspace is ready
    When I run the "windows_app_close_hung_up" flow
    Then the "windows_app_close_hung_up" flow should finish
