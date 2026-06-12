# Petro Seven assets

Coleccion curada de referencias visuales y evidencias de ejecucion.

Los archivos fuente originales permanecen sin cambios en:

- `../imagenes proyecto gas`
- `../TESTING PETRO SEVEN`

Las carpetas `evidence/` y `work/` se mantienen solo de forma local y no se publican en GitHub.

## Estructura

- `assets/automation/`: recortes usados por automatizacion visual.
- `evidence/login/`: evidencia local del flujo de login, recortada al viewport de la app.
- `evidence/happy-path/`: evidencia local del flujo principal, recortada al viewport de la app.
- `evidence/desktop/`: evidencia local del simulador de bomba, recortada al area relevante.

## Criterios aplicados

| Tipo | Formato | Dimensiones | Motivo |
| --- | --- | --- | --- |
| Referencia de automatizacion | PNG | Tamano original | Cambiarla puede romper el reconocimiento visual. |
| Pantalla de la app | PNG | 900 x 1600 | Conserva texto nitido y elimina franjas grises. |
| Evidencia del simulador | JPEG, calidad 88 | 2200 x 1500 | Reduce peso sin perder legibilidad. |

El conjunto revisado baja de aproximadamente **10.42 MiB** a **4.11 MiB**.

## Hallazgos

- `assets/automation/login_button.png` mide `123 x 21`. Es pequeno a proposito y no debe redimensionarse.
- Los nombres fuente `anydesk_opened.png` no describen lo que aparece en pantalla. Las copias curadas usan nombres basados en el estado visible.
- `evidence/happy-path/02-premium-click-overlay.png` sirve como evidencia de interaccion, pero el resaltado tapa parte de la interfaz. Debe reemplazarse por una captura posterior al clic.
- `06-payment-waiting.png` y `07-payment-waiting-progress.png` muestran estados distintos de la animacion de espera. Conservar ambos solo si se necesita probar el progreso visual.
- Las evidencias del simulador exponen una direccion IP y parte del escritorio. Conviene volver a capturarlas mostrando solo la ventana remota y ocultando la IP.
- La evidencia fuente de activacion de unidad expone nombre, correo e identificador de conexion remota. Se excluyo de esta coleccion y debe volver a capturarse.
- `evidence/login/03-employee-welcome.png` muestra el nombre visible del empleado de prueba. Debe sustituirse si la coleccion se compartira fuera del equipo.

## Reglas para nuevas evidencias

1. Capturar despues de que la accion termine y la pantalla quede estable.
2. No incluir credenciales, direcciones IP, notificaciones ni aplicaciones ajenas.
3. Evitar cursores, indicadores de clic y overlays, salvo que sean el objeto de la prueba.
4. Usar PNG para interfaces y JPEG de alta calidad para capturas completas de escritorio.
5. Nombrar con orden y estado visible: `NN-accion-o-resultado.ext`.
6. Mantener el viewport de la app en `900 x 1600` para que las comparaciones sean consistentes.
