@invoice
Feature: Invoice flow

  Scenario: Run invoice from Behave
    Given the automation workspace is ready
    When I run the "invoice" flow
    Then the "invoice" flow should finish
