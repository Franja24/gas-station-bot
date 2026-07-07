@petroseven_matrix
Feature: PetroSeven matrix coverage

  @petroseven_matrix_automated
  Scenario: Run matrix checkpoints already covered by bot flows
    Given the automation workspace is ready
    When I run these flows
      | case_id    | flow               | checkpoint                                                             |
      | CP_7LY_001 | benefits           | Inicio de sesión por teléfono de lealtad                               |
      | CP_AV_001  | login              | Inicio de sesión por credenciales estándar para empleado               |
      | CP_AV_002  | login_error        | Bloqueo de login con contraseña errónea                                |
      | CP_AV_003  | login_error        | Bloqueo de login con empleado inexistente o inactivo                   |
      | CP_AV_009  | windows_app        | Consulta de estado de surtidor con apoyo de simulador                  |
      | CP_AV_010  | premium            | Catálogo por bomba y selección de producto                             |
      | CP_AV_012  | change_type_charge | Envío de solicitud por volumen/monto                                   |
      | CP_KON_001 | invoice            | Generación de factura con validación externa pendiente                 |
      | CP_KIOS_001 | premium           | Venta sin inicio por lealtad                                           |
      | CP_KIOS_002 | benefits          | Despliegue de opciones de lealtad por acceso directo                   |
      | CP_KIOS_003 | benefits          | Despliegue de opciones de lealtad dentro del flujo de carga            |
      | CP_KIOS_008 | normal_magna_1250 | Carga por importe monetario                                            |
      | CP_KIOS_011 | change_type_charge | Cambio de combustible en pantalla de monto                             |
      | CP_KIOS_021 | windows_app       | Check-in/preautorización con apoyo de simulador                        |
      | CP_KIOS_030 | sevenly           | Finalización de venta sin imprimir ticket                              |
      | CP_KIOS_031 | print             | Finalización con impresión de ticket y validación física pendiente     |
      | CP_KIOS_032 | invoice_full      | Finalización con ticket y factura con validación externa pendiente     |
    Then the selected flows should finish

  @petroseven_matrix_assisted @bot_humano
  Scenario: Register matrix checkpoints covered by bot plus human validation
    When I register these assisted checkpoints
      | case_id     | checkpoint                                            | bot_scope                                  | human_scope                                      |
      | CP_AV_004   | Inicio de sesión por RFID para empleado              | Evidencia visual de login/menú             | Lectura RFID física y respuesta Avalon           |
      | CP_AV_005   | Login con RFID no válida o inactiva                  | Evidencia visual de error                  | Presentar tarjeta física no válida               |
      | CP_AV_006   | Cierre de sesión para empleado por RFID              | Evidencia visual de retorno a login        | Escaneo RFID/cierre físico                       |
      | CP_AV_007   | Cambio de empleado                                   | Evidencia visual de transición de empleado | Validación humana del cambio de empleado         |
      | CP_AV_016   | Funcionalidad de RFC                                 | Navegación/captura en facturación          | Validar datos devueltos por Avalon               |
      | CP_AV_017   | Rechazo por RFC inexistente o inactivo               | Navegación/captura en facturación          | Validar respuesta negativa de Avalon             |
      | CP_KIOS_005 | Cancelación de operación en PinPad                   | Evidencia visual antes/después             | Cancelación física en PinPad                     |
      | CP_KIOS_007 | Reintento de impresión por fallo                     | Navegación a impresión                     | Provocar/validar fallo físico de impresora       |
      | CP_KIOS_012 | Cierre de turno por misma tarjeta de empleado        | Evidencia visual de pantalla de sesión     | Tarjeta física de empleado                       |
      | CP_KIOS_013 | Pantalla de cambio de empleado                       | Evidencia visual de pantalla de sesión     | Validación humana/RFID del empleado              |
    Then the assisted checkpoints should be documented
