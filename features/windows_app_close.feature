@windows_app_close @windows_app_clos
Feature: Windows App close flow

  Scenario: Close the pump simulator from Behave
    Given the automation workspace is ready
    When I run the "windows_app_close" flow
    Then the "windows_app_close" flow should finish
