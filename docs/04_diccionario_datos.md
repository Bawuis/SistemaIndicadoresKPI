# Diccionario de Datos — SistemaIndicadoresKPI

## source_A.xlsx — Reporte Operacional

| # | Columna | Tipo | Obligatorio | Descripcion | Regla de Validacion |
|---|---|---|---|---|---|
| 1 | ID_Operacion | String | SI | Identificador unico de la operacion | No nulo, No duplicado |
| 2 | Fecha | Date | SI | Fecha de ejecucion | Formato YYYY-MM-DD, No nulo |
| 3 | Unidad | String | SI | Unidad organizacional responsable | No nulo |
| 4 | Valor_Real | Float | SI | Valor ejecutado o medido | Mayor a 0, No nulo |
| 5 | Responsable | String | SI | Nombre del responsable | No nulo |

Ejemplo:
ID_Operacion | Fecha      | Unidad       | Valor_Real | Responsable
OP-001       | 2026-04-01 | Ventas Norte | 850.00     | Juan Perez
OP-002       | 2026-04-01 | Ventas Sur   | 1200.50    | Maria Lopez

## source_B.xlsx — Reporte de Objetivos

| # | Columna | Tipo | Obligatorio | Descripcion | Regla de Validacion |
|---|---|---|---|---|---|
| 1 | ID_Operacion | String | SI | Llave de cruce con source_A | No nulo |
| 2 | Periodo | String | SI | Periodo al que corresponde la meta | No nulo |
| 3 | Valor_Meta | Float | SI | Meta o presupuesto asignado | Distinto de 0, No nulo |
| 4 | Categoria | String | SI | Clasificacion de la operacion | No nulo |
| 5 | Estado | String | SI | Estado actual | Activo, En Progreso, Cerrado |

## Columnas Calculadas en output_reporte.xlsx

| Columna | Formula | Descripcion |
|---|---|---|
| Pct_Cumplimiento | (Valor_Real / Valor_Meta) * 100 | Porcentaje de cumplimiento |
| Variacion_Abs | Valor_Real - Valor_Meta | Desviacion absoluta respecto a la meta |
| Semaforo | Condicional | Optimo >=90% / En Riesgo >=70% / Critico <70% |

## Reglas de Calidad de Datos (DQ Rules)

| ID | Regla | Campo | Accion si Falla |
|---|---|---|---|
| DQ-01 | ID_Operacion no puede ser nulo | source_A, source_B | Rechazar registro |
| DQ-02 | Valor_Real debe ser mayor a 0 | source_A | Rechazar registro |
| DQ-03 | Valor_Meta no puede ser 0 ni nulo | source_B | Pct_Cumplimiento = NULL |
| DQ-04 | Fecha debe tener formato valido | source_A | Rechazar registro |
| DQ-05 | No se permiten duplicados en ID_Operacion | source_A, source_B | Conservar primer registro |
| DQ-06 | Columnas requeridas deben existir | Todos | Detener pipeline y mover a /error |

*Documento generado automaticamente — Pipeline ETL v1.0.0*

---