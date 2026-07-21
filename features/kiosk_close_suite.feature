@kiosk_close_suite @ordered
Feature: Recover the kiosk after it is closed during a fuel sale

  Background:
    Given the automation workspace is ready
    And the remote desktop app is "RustDesk"

  Scenario: Case 1 - Close the kiosk at the payment screen
    Given the kiosk application is open and ready
    And the employee session is active
    When I start a "Magna" sale for 100 pesos and reach the payment terminal
    And I close the kiosk application at the payment screen
    Then the kiosk application should be closed
    When I reopen the kiosk application
    Then the employee login screen should be visible

  Scenario: Case 2 - Close the kiosk with the hose unhooked
    Given the employee session is active
    When I start a "Magna" sale for 150 pesos and wait for payment approval
    Then the payment should be approved
    When I unhook the hose and close the kiosk application
    And I reopen the kiosk application
    And I activate the unit for recovery
    Then the pump out of service screen should be visible
    When I cancel the latest transaction for 150 pesos
    And I hang up the hose and reset the OpenPOS pump
    And I continue the active kiosk session
    Then the fuel product selection should be visible

  Scenario: Case 3 - Close the kiosk while fuel is dispensing
    Given the employee session is active
    And the fuel product selection is visible
    When I start a "Premium" sale for 200 pesos and reach the dispatch instructions
    Then the payment should be approved for the 200 peso sale
    When I unhook the hose in the pump simulator
    And I press the trigger to start fuel dispensing
    And I return to the kiosk and close the application
    And I hang up the hose in the pump simulator
    And I reopen the kiosk application
    And I log in to recover the pending transaction
    And I recover the latest transaction for 200 pesos
    Then the fuel product selection should be visible
