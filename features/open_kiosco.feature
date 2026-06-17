@open_kiosco
Feature: Open Kiosco flow

  Scenario: Open the POS kiosco from Behave
    Given the automation workspace is ready
    When I run the "open_kiosco" flow
    Then the "open_kiosco" flow should finish
