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
- ReportLab

## Instalación

Crear entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Ejecución con Behave

Correr todos los flujos:

```bash
behave
```

Correr un flujo específico:

```bash
behave --tags @login
behave --tags @premium
behave --tags @sevenly
behave --tags @invoice
behave --tags @windows_app
```

El tag `@sevenly` corre el camino completo: login, compra premium, simulador de bomba y factura.

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
## reportlab
Genera el reporte PDF con las evidencias de la corrida.
