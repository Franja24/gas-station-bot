@happy_path_rustdesk @rustdesk
Feature: Happy path flow with RustDesk

  Background:
    Given the remote desktop app is "RustDesk"
    And the automation workspace is ready
    When I run the "open_kiosco" flow
    Then the "login_button" asset should be visible

  Scenario: Run migrated happy path from Behave using RustDesk
    When I run these flows
      | flow              |
      | login             |
      | magna             |
      | premium           |
      | sevenly_login     |
      | windows_app       |
      | windows_app_close |
      | invoice           |
      | print             |
    Then the selected flows should finish
