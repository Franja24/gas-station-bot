@happy_path
Feature: Happy path flow

  Scenario: Run migrated happy path from Behave
    Given the automation workspace is ready
    When I run these flows
      | flow              |
      | open_kiosco       |
      | login             |
      | magna             |
      | premium           |
      | sevenly_login     |
      | windows_app       |
      | windows_app_close |
      | invoice           |
      | print             |
    Then the happy path should finish
