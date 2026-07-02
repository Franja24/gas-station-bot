@happy_path
Feature: Happy path flow

  Background:
    Given the automation workspace is ready
    When I run the "open_kiosco" flow
    Then the "open_kiosco" flow should finish

  Scenario: Run migrated happy path from Behave
    When I run these flows
      | flow                    |
      | normal_magna_1250       |
      | normal_premium_500      |
      | sevenly_magna_liters_20 |
    Then the selected flows should finish
