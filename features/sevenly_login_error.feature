Feature: Sevenly Login Error

  Scenario: Phone number is not registered in Sevenly benefits

    Given the application is ready

    When we click on the "sevenly" button

    And we click on the "telefon_number" button

    And we enter phone number "5531044840"

    And we click on the "continue" button

    Then the "no_registered_benefits_number" error message should be displayed
