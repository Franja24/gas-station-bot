@windows_app_hang_up
Feature: Windows app hang up flow

  Scenario: Hang up hose from Behave
    Given the automation workspace is ready
    When I run the "windows_app_hang_up" flow
    Then the "windows_app_hang_up" flow should finish
