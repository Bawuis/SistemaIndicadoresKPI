# 📋 Documentación Funcional — Flujo de Trabajo End-to-End

## Resumen Ejecutivo

El sistema monitorea carpetas de entrada en tiempo real. Al detectar la presencia de **dos archivos Excel de origen**, dispara automáticamente un pipeline ETL que extrae, transforma, calcula métricas y genera un reporte consolidado en una carpeta de salida, archivando los insumos procesados.

---

## Fuentes de Datos Definidas

| Archivo | Nombre Lógico | Descripción | Columnas Clave |
|---|---|---|---|
| `source_A.xlsx` | **Reporte Operacional** | Datos de ejecución/actividad | `ID_Operacion`, `Fecha`, `Unidad`, `Valor_Real`, `Responsable` |
| `source_B.xlsx` | **Reporte de Objetivos** | Metas y presupuesto asignado | `ID_Operacion`, `Periodo`, `Valor_Meta`, `Categoria`, `Estado` |

> 🔑 La columna **`ID_Operacion`** es la llave de cruce (*JOIN key*) entre ambas fuentes.

---

## Flujo de Trabajo — Paso a Paso

### FASE 1 — Monitoreo (Event-Driven)
- El sistema ejecuta un **watcher** sobre la carpeta `/input`.
- El intervalo de verificación es de **60 segundos**.
- El pipeline se dispara **únicamente** cuando ambos archivos (`source_A.xlsx` y `source_B.xlsx`) están presentes simultáneamente.

### FASE 2 — Extracción
- Se cargan ambos archivos Excel en memoria como DataFrames.
- Se valida que las columnas requeridas existan y tengan el tipo de dato correcto.
- Si la validación falla: se genera un log de error, se notifica al usuario y los archivos se mueven a `/error`.

### FASE 3 — Transformación y Limpieza
- Conversión de tipos: fechas, numéricos.
- Eliminación de duplicados por `ID_Operacion`.
- Filtrado de registros con `Valor_Real <= 0`.
- Eliminación de nulos en columnas críticas de `source_B`.

### FASE 4 — Consolidación
- Se realiza un **LEFT JOIN** entre `source_A` y `source_B` usando `ID_Operacion` como llave primaria.
- Resultado: un DataFrame unificado con todas las columnas de ambas fuentes.

### FASE 5 — Cálculo de Métricas
| Métrica | Fórmula | Descripción |
|---|---|---|
| `Pct_Cumplimiento` | `(Valor_Real / Valor_Meta) * 100` | Porcentaje de cumplimiento por operación |
| `Variacion_Abs` | `Valor_Real - Valor_Meta` | Desviación absoluta respecto a la meta |
| `Semaforo` | Clasificación condicional | 🟢 Óptimo ≥90% / 🟡 En Riesgo ≥70% / 🔴 Crítico <70% |
| `Promedio_Cumplimiento` | `PROMEDIO(Pct_Cumplimiento)` | KPI global del período |
| `Total_Valor_Real` | `SUMA(Valor_Real)` | Total ejecutado |
| `Total_Valor_Meta` | `SUMA(Valor_Meta)` | Total presupuestado |

### FASE 6 — Generación del Reporte
- Se exporta un archivo Excel con **3 hojas**:
  - `📊 Dashboard` — KPIs globales y resumen ejecutivo
  - `📋 Detalle` — Tabla consolidada con semáforo condicional
  - `ℹ️ Metadata` — Log del proceso (timestamp, filas procesadas, errores)
- Nombre del archivo: `output_reporte_YYYYMMDD_HHMMSS.xlsx`
- Destino: carpeta `/output`

### FASE 7 — Archivado
- Los archivos fuente se mueven a `/archive/{fecha}/` con timestamp en el nombre.
- Se registra entrada de éxito en el log del sistema.
- El watcher reinicia el ciclo de monitoreo.

---

## Reglas de Negocio

1. Si `Valor_Meta = 0`, el campo `Pct_Cumplimiento` se asigna como `NULL` para evitar división por cero.
2. Solo se procesan registros donde `Estado` en `source_B` sea "Activo" o "En Progreso".
3. El reporte se genera con el timestamp del momento de ejecución, garantizando unicidad del nombre.
4. Los archivos en `/error` NO se archivan ni eliminan automáticamente — requieren revisión manual.

---

*Documento generado automáticamente — Pipeline ETL v1.0.0*