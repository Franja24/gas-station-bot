@change_type_charge @kios_011
Feature: Change type charge flow

  Scenario: Run change type charge from Behave
    Given the automation workspace is ready
    When I run the "change_type_charge" flow
    Then the "change_type_charge" flow should finish
