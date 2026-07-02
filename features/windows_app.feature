@windows @windows_app
Feature: Windows App flow

  Scenario: Run Windows App pump simulator from Behave
    Given the automation workspace is ready
    When I run the "windows app" flow
    Then the "windows app" flow should finish
