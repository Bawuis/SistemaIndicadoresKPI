# SistemaIndicadoresKPI

Pipeline ETL en Python para consolidar 3 archivos Excel en una plantilla predefinida de calculo de horas.

## 1) Arquitectura de carpetas recomendada

Este proyecto queda funcionando en:

`C:/Users/carlo/OneDrive/Desktop/kpi/SistemaIndicadoresKPI`

Carpetas operativas:

- `data/input`: donde debes colocar tus 3 archivos Excel de entrada.
- `data/input_secundario`: entrada dedicada para el segundo proceso.
- `data/plantillas`: plantillas Excel con columnas base.
- `data/processing`: carpeta temporal del flujo.
- `data/output`: reportes generados.
- `data/output_secundario`: salida dedicada para el segundo proceso.
- `data/archive`: historico de fuentes procesadas.
- `data/error`: archivos con error de estructura o lectura.
- `data/logs`: logs del ETL.

## 2) Requisitos

- Python 3.10 o superior.
- Dependencias del archivo `requirements.txt`.

Instalacion:

```bash
pip install -r requirements.txt
```

## 3) Estructura esperada de los archivos de entrada

El proceso identifica automaticamente los archivos por palabras clave en el nombre (no por nombre exacto):

- Archivo A: contiene `elearning`
- Archivo B: contiene `filesJMC`
- Archivo C: contiene `participantes`

Tambien detecta la plantilla en `data/plantillas` por keyword `calculo horas 2026`.

## 4) Reglas de extraccion y pegado

Se copian solo valores (sin encabezados):

1. Desde archivo `elearning`:
   - Columna A
   - Columna B
   - Columna I

2. Desde archivo `filesJMC`:
   - Columna A
   - Columna D
   - Columna M

3. Desde archivo `participantes`:
   - Encabezados en fila 8, datos desde fila 9
   - Columna E (`login`)
   - Columna AI (`Training name`)
   - Columna AK (`End date of the date`) convertida a fecha corta (sin hora)
   - Columna AO (`Number of training hours`)

4. Consolidacion:
   - Primero se pega `elearning`
   - Debajo, de forma continua, se pega `filesJMC`
   - Luego, de forma continua, se pega `participantes`

Destino en plantilla:

- Encabezados objetivo estan en fila 2
- Columnas destino: B, E y H (con intercambio E/H respecto al origen)
- Inicio de datos: fila 3
- Para `participantes`, la columna AO se pega en la columna J de la plantilla

Importante:

- Se ignoran archivos temporales de Excel que empiezan por `~$`.
- El archivo de `participantes` se valida por presencia y se archiva al final del proceso.

## 5) Paso a paso para ejecutar correctamente

1. Abre terminal en `C:/Users/carlo/OneDrive/Desktop/kpi/SistemaIndicadoresKPI`.
2. Instala dependencias:
   `pip install -r requirements.txt`
3. Coloca en `data/input` los 3 archivos (con keywords `elearning`, `filesJMC`, `participantes`).
4. Verifica que la plantilla exista en `data/plantillas` y contenga encabezados en fila 2.
5. Ejecuta una corrida unica:
   `python main.py --once`
6. Revisa resultado en `data/output`.
7. Verifica trazabilidad en `data/logs`.
8. Confirma que las fuentes procesadas se movieron a `data/archive/<fecha>`.

## 6) Ejecucion en modo monitor continuo (opcional)

Este modo observa `data/input` y dispara automaticamente el proceso cuando detecta los 3 archivos por keyword.

```bash
python main.py
```

## 7) Resultado esperado

Se genera un Excel tipo:

- `Calculo Horas 2026 ... _consolidado_YYYYMMDD_HHMMSS.xlsx`

Comportamiento esperado:

- Datos pegados desde B3, E3 y H3 en adelante.
- Formulas arrastradas hasta la ultima fila con datos nuevos.
- En columna J, las formulas solo se mantienen para filas de `elearning` y `filesJMC`; en filas de `participantes` se conserva el valor crudo de AO.
- Archivos de entrada movidos a `data/archive/<fecha>`.

## 8) Solucion de problemas rapida

- Si falla lectura de Excel: valida extension `.xlsx` y que no este bloqueado por otra aplicacion.
- Si no detecta archivo: revisa que el nombre incluya la keyword esperada.
- Si no pega en columnas correctas: valida que la plantilla tenga encabezados en fila 2 y estructura de destino B/E/H.
- Si no genera salida: revisa `data/logs/etl_YYYY-MM-DD.log`.

## 9) Proceso secundario automatico (output -> output_secundario)

Al finalizar la consolidacion principal, el sistema ejecuta automaticamente un segundo proceso:

1. Toma el archivo consolidado recien generado en `data/output`.
2. Copia el rango desde columna B hasta P, desde la fila 3 hasta la ultima fila con datos.
3. Busca en `data/input_secundario` el archivo cuyo nombre contenga la keyword `horas entrenamiento 2026`.
4. En ese archivo, hoja `Reporte horas`, pega la informacion en columnas A:O iniciando en fila 2.
5. El pegado se hace de forma continua, inmediatamente despues de la ultima fila ocupada existente (lista continua).
6. Genera el nuevo archivo en `data/output_secundario` con sufijo `_actualizado_YYYYMMDD_HHMMSS.xlsx`.
