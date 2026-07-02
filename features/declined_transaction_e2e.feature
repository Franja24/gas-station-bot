@declined_transaction_e2e
Feature: Declined transaction e2e flow

  Scenario: Create a declined payment and open its request metadata
    Given the automation workspace is ready
    When I run the "declined_transaction_e2e" flow
    Then the "declined_transaction_e2e" flow should finish
