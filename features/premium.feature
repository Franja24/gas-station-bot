Feature: Premium Purchase

  Scenario: Purchase Premium Fuel

    Given the application is ready

    When we click on the "premium" button

    And we click on the "amount_1250_premium" button

    And we click on the "continue" button

    And we click on the "no_benefits" button

    And we click on the "continue" button

    Then the happy path should be completed