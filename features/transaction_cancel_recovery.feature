@transaction_cancel_recovery
Feature: Transaction cancel recovery flow

  Scenario: Cancel recovered transaction from Behave
    Given the automation workspace is ready
    When I run the "transaction_cancel_recovery" flow
    Then the "transaction_cancel_recovery" flow should finish
