# Gas Station Automation Bot

Automatización visual para flujo de compra en POS de gasolinera usando Python, PyAutoGUI, OpenCV y Behave.

## Tecnologías usadas

- Python 3.11
- PyAutoGUI
- OpenCV
- Pillow
- MSS
- NumPy
- Pynput
- Behave

## Instalación

Crear entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

## Librerías
pyautogui
Se usa para mover el mouse, capturar pantalla y apoyar la automatización visual.
## opencv-python
Permite buscar imágenes en pantalla usando confidence.
## pillow
Soporte para manejo de imágenes y screenshots.
## mss
Captura de pantalla rápida.
## numpy
Procesamiento de imágenes junto con OpenCV.
## pynput
Se usa para enviar clicks más compatibles con AnyDesk/RustDesk.
## behave
Permite ejecutar escenarios BDD escritos en lenguaje tipo Gherkin.

## Flujo recomendado con Git

Crear una rama propia para calibrar coordenadas:

```bash
git checkout -b feature/calibracion-mi-maquina

## Modo seguro de clic

Los objetivos usados por los flujos actuales hacen clic mediante coordenadas
calibradas para una pantalla de `1280x800`. Las coordenadas se ajustan en:

- `config/coordinates.py`
- `config/login_keyboard.py`
- `config/phone_keyboard.py`
- `config/rfc_keyboard.py`

Si la resolución actual no coincide con la calibrada, el flujo se detiene antes
de hacer clic.

La detección por imagen queda como respaldo para objetivos sin coordenadas. En
ese modo se exige una confianza mínima de `0.80` y dos detecciones consecutivas
en la misma posición:

```python
click_image(
    "new_button.png",
    confidence=0.90,
    use_coordinates=False,
)
```

## Resultado del caso

Ejecutar el caso configurado en `main.py`:

```bash
python main.py
python main.py e2e
python main.py login
python main.py magna
python main.py premium
python main.py sevenly_login
python main.py benefits
python main.py windows
python main.py invoice
```

`python main.py` y `python main.py e2e` ejecutan el flujo completo:

```text
01_login -> 02_premium -> 03_windows -> 04_invoice
```

Si una etapa falla, las siguientes no se ejecutan. El `result.json` y el PDF
indican el estado y duración de cada etapa. Las capturas del flujo completo
incluyen el nombre de su etapa para evitar que archivos repetidos se
sobrescriban.

Al terminar, la consola muestra `RESULTADO: PASSED` o `RESULTADO: FAILED`.
También se crean estos archivos dentro de `Evidencias/run_<fecha>/`:

- `result.json`: estado, duración y error.
- `execution_report.pdf`: reporte con estado y capturas.
- `screenshots/FAILED_error.png`: pantalla del momento del fallo, cuando aplica.

El proceso devuelve código `0` para `PASSED` y código `1` para `FAILED`.
`PASSED` significa que la automatización terminó sin excepciones y pasó todas
las validaciones funcionales configuradas. El caso de login ya verifica que
aparezca `premium.png` después de iniciar.

Para agregar una validación funcional a otro caso:

```python
assert_image_visible("expected_final_screen.png", timeout=15)
```
