# SistemaIndicadoresKPI

Pipeline ETL en Python para consolidar 2 archivos Excel, calcular metricas KPI y generar un reporte final en Excel.

## 1) Arquitectura de carpetas recomendada

Este proyecto queda funcionando en:

`C:/Users/carlo/OneDrive/Desktop/kpi/SistemaIndicadoresKPI`

Carpetas operativas:

- `data/input`: donde debes colocar tus 2 archivos Excel.
- `data/plantillas`: plantillas Excel con columnas base.
- `data/processing`: carpeta temporal del flujo.
- `data/output`: reportes generados.
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

## 3) Estructura esperada de los 2 Excel

### Archivo 1: `source_A.xlsx`

Columnas obligatorias:

- `ID_Operacion`
- `Fecha`
- `Unidad`
- `Valor_Real`
- `Responsable`

### Archivo 2: `source_B.xlsx`

Columnas obligatorias:

- `ID_Operacion`
- `Periodo`
- `Valor_Meta`
- `Categoria`
- `Estado`

Importante:

- Debes respetar exactamente los nombres de archivo y columnas.
- Si no coinciden, el archivo se movera a `data/error`.

## 4) Paso a paso para ejecutar correctamente

1. Abre terminal en `C:/Users/carlo/OneDrive/Desktop/kpi/SistemaIndicadoresKPI`.
2. Instala dependencias:
   `pip install -r requirements.txt`
3. Abre las plantillas en `data/plantillas` y pega tus datos.
4. Guarda o copia tus 2 archivos en `data/input` con estos nombres:
   `source_A.xlsx` y `source_B.xlsx`.
5. Ejecuta una corrida unica:
   `python main.py --once`
6. Revisa resultado en `data/output`.
7. Verifica trazabilidad en `data/logs`.
8. Confirma que fuentes procesadas se movieron a `data/archive/<fecha>`.

## 5) Ejecucion en modo monitor continuo (opcional)

Este modo observa `data/input` y dispara automaticamente el proceso cuando detecta ambos archivos.

```bash
python main.py
```

## 6) Resultado esperado

Se genera un Excel tipo:

- `output_reporte_YYYYMMDD_HHMMSS.xlsx`

Con hojas:

- `Dashboard KPI`
- `Detalle`
- `Metadata`

## 7) Solucion de problemas rapida

- Si falla lectura de Excel: valida extension `.xlsx` y que no este bloqueado por otra aplicacion.
- Si faltan columnas: corrige encabezados exactamente como en la seccion 3.
- Si no genera salida: revisa `data/logs/etl_YYYY-MM-DD.log`.
