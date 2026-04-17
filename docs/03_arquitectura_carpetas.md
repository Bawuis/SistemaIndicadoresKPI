# Arquitectura de Carpetas — SistemaIndicadoresKPI

## Estructura Completa

```
SistemaIndicadoresKPI/
|-- main.py
|-- config.yaml
|-- requirements.txt
|-- src/
|   |-- config_loader.py
|   |-- monitor.py
|   |-- extractor.py
|   |-- transformador.py
|   |-- calculador_metricas.py
|   |-- generador_reporte.py
|   `-- pipeline.py
|-- docs/
|   |-- 01_documentacion_funcional.md
|   |-- 02_diagrama_flujo.md
|   `-- 03_arquitectura_carpetas.md
|-- input/       # ZONA DE CARGA
|-- processing/  # ZONA TEMPORAL
|-- output/      # REPORTES GENERADOS
|-- archive/     # HISTORICO
|-- logs/        # TRAZABILIDAD
`-- error/       # FALLOS
```

## Descripcion por Zona

| Carpeta | Rol | Acceso |
|---|---|---|
| /input | Zona de carga, monitoreada en tiempo real | Usuario |
| /processing | Zona temporal durante el procesamiento | Sistema |
| /output | Reportes finales listos para consumo | Usuario |
| /archive | Historico inmutable, organizado por fecha YYYY-MM-DD | Solo lectura |
| /logs | Trazabilidad completa, rotacion diaria 30 dias | Administrador |
| /error | Archivos que fallaron validacion, requieren revision manual | Administrador |

## Reglas
1. /input es la unica carpeta donde el usuario deposita archivos.
2. /output nunca se modifica manualmente.
3. /archive se organiza por fecha YYYY-MM-DD.
4. /error requiere intervencion manual.
5. Los logs rotan diariamente y se retienen 30 dias.

## Convenciones de Nombres

| Tipo | Patron | Ejemplo |
|---|---|---|
| Fuente | source_{letra}.xlsx | source_A.xlsx |
| Reporte | output_reporte_{YYYYMMDD}_{HHMMSS}.xlsx | output_reporte_20260417_143022.xlsx |
| Archivado | {nombre}_{YYYYMMDD}_{HHMMSS}.xlsx | source_A_20260417_143022.xlsx |
| Log | etl_{YYYY-MM-DD}.log | etl_2026-04-17.log |