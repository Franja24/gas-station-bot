Feature: Magna Purchase

  Scenario: Purchase Magna Fuel

    Given the application is ready

    When we click on the "magna" button

    And we click on the "amount_1250" button

    And we click on the "continue" button

    And we click on the "card" button

    Then the happy path should be completed
