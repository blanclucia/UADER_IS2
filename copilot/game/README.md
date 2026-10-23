# Esquivá Meteoritos

Juego 2D sencillo hecho con Python y Pygame. Controlá la nave y esquivá los meteoritos el mayor tiempo posible. Todos los elementos visuales se dibujan con figuras de Pygame: no hacen falta imágenes ni archivos de sonido.

## Requisitos

- Python 3.9 o posterior.
- VS Code con una terminal integrada (o cualquier terminal).

## Preparar el entorno

Abrí la carpeta `copilot/game` en VS Code y ejecutá los comandos correspondientes en la terminal integrada.

### macOS y Linux

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Si PowerShell no permite activar el entorno, podés usar el Símbolo del sistema (CMD):

```bat
.venv\Scripts\activate.bat
```

Con el entorno activado, también podés elegir el intérprete `.venv` en VS Code: abrí la paleta de comandos, buscá **Python: Select Interpreter** y seleccioná el que está dentro de `.venv`.

## Controles

- **Flecha izquierda** o **A**: mover la nave a la izquierda.
- **Flecha derecha** o **D**: mover la nave a la derecha.
- **R**: reiniciar después de perder.
- **Escape**: salir.

El puntaje cuenta los segundos sobrevividos. Los meteoritos aparecen cada vez más seguido y se vuelven más rápidos con el paso del tiempo.

## Ajustar la dificultad

En la parte superior de `main.py` están las constantes principales:

- `VELOCIDAD_NAVE`: velocidad horizontal de la nave.
- `INTERVALO_METEORITOS_INICIAL`: demora inicial entre meteoritos; un valor menor aumenta la frecuencia.
- `INTERVALO_METEORITOS_MINIMO`: límite de la demora cuando la dificultad ya aumentó.
- `AUMENTO_DIFICULTAD_POR_SEGUNDO`: ritmo al que sube la dificultad.
- `VELOCIDAD_METEORITO_MINIMA` y `VELOCIDAD_METEORITO_MAXIMA`: rango de velocidad inicial de los meteoritos.
- `PROBABILIDAD_METEORITO_RAPIDO`: posibilidad de que un meteorito aparezca más rápido (por ejemplo, `0.15` equivale al 15 %).
- `MULTIPLICADOR_METEORITO_RAPIDO`: cuánto más rápido será ese meteorito.
- `FPS`: límite de fotogramas por segundo.

La partida nueva vuelve a crear la nave, el puntaje, la dificultad y la lista de meteoritos. Las estrellas son parte del fondo y continúan moviéndose durante toda la ejecución.
