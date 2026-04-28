# Arquitectura de Carpetas Recomendada - SistemaIndicadoresKPI

## Ubicacion Base

Ruta base solicitada:

`C:/Users/carlo/OneDrive/Desktop/kpi`

## Estructura Recomendada

```
kpi/
`-- SistemaIndicadoresKPI/
	|-- main.py
	|-- config.yaml
	|-- requirements.txt
	|-- README.md
	|-- src/
	|   |-- __init__.py
	|   |-- config_loader.py
	|   |-- extractor.py
	|   |-- transformador.py
	|   |-- calculador_metricas.py
	|   |-- generador_reporte.py
	|   |-- pipeline.py
	|   `-- monitor.py
	|-- docs/
	|   |-- 01_documentacion_funcional.md
	|   |-- 02_diagrama_flujo.md
	|   |-- 03_arquitectura_carpetas.md
	|   |-- 04_diccionario_datos.md
	|   |-- 05_guia_configuracion.md
	|   |-- 06_manejo_errores.md
	|   `-- 07_guia_despliegue.md
	`-- data/
		|-- input/       # Aqui colocas los 2 Excel de entrada
		|-- processing/  # Espacio temporal del proceso
		|-- output/      # Reportes Excel generados
		|-- archive/     # Historial de fuentes procesadas por fecha
		|-- logs/        # Logs diarios del proceso ETL
		`-- error/       # Archivos con validacion fallida
```

## Reglas Operativas

1. Solo se cargan archivos en `data/input`.
2. Los archivos de entrada deben llamarse `source_A.xlsx` y `source_B.xlsx`.
3. El proceso genera reporte en `data/output` y luego mueve fuentes a `data/archive`.
4. Si falta esquema o hay error de lectura, el archivo se mueve a `data/error`.
5. Los logs se guardan en `data/logs` con rotacion diaria.

## Convenciones de Nombres

| Tipo | Patron | Ejemplo |
|---|---|---|
| Entrada A | source_A.xlsx | source_A.xlsx |
| Entrada B | source_B.xlsx | source_B.xlsx |
| Reporte | output_reporte_YYYYMMDD_HHMMSS.xlsx | output_reporte_20260422_101500.xlsx |
| Archivado | nombre_YYYYMMDD_HHMMSS.xlsx | source_A_20260422_101500.xlsx |
| Log | etl_YYYY-MM-DD.log | etl_2026-04-22.log |