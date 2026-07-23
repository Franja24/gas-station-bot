@petroseven_matrix_first_set
Feature: PetroSeven first matrix set

  Scenario: Run the first four matrix checkpoints in order
    Given the automation workspace is ready
    When I run these flows
      | case_id    | flow                 | checkpoint                                               |
      | CP_AV_002  | login_error          | Bloqueo de login con contraseña errónea                  |
      | CP_AV_003  | login_inactive_error | Bloqueo de login con empleado inexistente o inactivo     |
      | CP_AV_001  | login                | Inicio de sesión por credenciales estándar para empleado |
      | CP_7LY_001 | benefits             | Inicio de sesión por teléfono de lealtad                 |
    Then the selected flows should finish
