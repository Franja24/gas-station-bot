@unhook_hose_before_payment_approval
Feature: Unhook hose before payment approval

  Scenario: Unhook the hose while the payment terminal is ready but not yet approved
    Given the automation workspace is ready
    When I run the "unhook_hose_before_payment_approval" flow
    Then the "unhook_hose_before_payment_approval" flow should finish
