@normal_magna_continue
Feature: Continue normal Magna flow

  Scenario: Continue a normal Magna charge from benefits or payment
    Given the automation workspace is ready
    When I run the "normal_magna_continue" flow
    Then the "normal_magna_continue" flow should finish
