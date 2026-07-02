@declined_transaction_request
Feature: Declined transaction request flow

  Scenario: Open the request metadata for the latest declined transaction
    Given the automation workspace is ready
    When I run the "declined_transaction_request" flow
    Then the "declined_transaction_request" flow should finish
