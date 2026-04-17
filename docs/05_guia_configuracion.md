# Guia de Configuracion — config.yaml

Este archivo es el unico punto de configuracion del pipeline. Todos los parametros se controlan desde aqui sin modificar el codigo fuente.

## Referencia de Parametros

### Seccion pipeline
```yaml
pipeline:
  nombre: "ETL_Consolidacion_Metricas"
  version: "1.0.0"
  autor: "SistemaIndicadoresKPI"
```
| Parametro | Requerido | Descripcion |
|---|---|---|
| nombre | SI | Identificador logico. Aparece en reportes y logs |
| version | SI | Version semantica MAJOR.MINOR.PATCH |
| autor | NO | Propietario del proceso |

### Seccion rutas
```yaml
rutas:
  input:      "./input"
  processing: "./processing"
  output:     "./output"
  archive:    "./archive"
  logs:       "./logs"
  error:      "./error"
```
Todas las rutas pueden ser relativas (desarrollo) o absolutas (produccion).

### Seccion join
```yaml
join:
  llave_primaria: "ID_Operacion"
  tipo: "left"
```
| tipo | Comportamiento |
|---|---|
| left | Conserva todos los registros de source_A aunque no tengan meta |
| inner | Solo registros presentes en AMBAS fuentes |
| outer | Todos los registros de ambas fuentes |

### Seccion metricas
```yaml
metricas:
  cumplimiento_optimo: 90
  cumplimiento_en_riesgo: 70
```
Logica del Semaforo:
- Pct >= cumplimiento_optimo = Optimo
- Pct >= cumplimiento_en_riesgo = En Riesgo
- Pct < cumplimiento_en_riesgo = Critico

### Seccion monitoreo
```yaml
monitoreo:
  intervalo_segundos: 60
  notificacion_email: "equipo@empresa.com"
```

## Configuraciones por Ambiente

Desarrollo:
```yaml
monitoreo:
  intervalo_segundos: 10
```

Produccion:
```yaml
rutas:
  input: "D:/ETL/Produccion/input"
  output: "D:/ETL/Produccion/output"
monitoreo:
  intervalo_segundos: 60
  notificacion_email: "operaciones@empresa.com"
```

*Documento generado automaticamente — Pipeline ETL v1.0.0*

---