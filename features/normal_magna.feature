@normal_magna
Feature: Normal Magna flow

  Scenario: Run a normal Magna charge from product selection
    Given the automation workspace is ready
    When I run the "normal_magna" flow
    Then the "normal_magna" flow should finish
