# Manejo de Errores y Troubleshooting — SistemaIndicadoresKPI

## Catalogo de Errores

### Errores de Configuracion
| Codigo | Error | Causa | Solucion |
|---|---|---|---|
| ERR-CFG-01 | config.yaml no encontrado | Archivo no existe en directorio raiz | Verificar que config.yaml este junto a main.py |
| ERR-CFG-02 | KeyError en seccion del config | Falta seccion requerida | Comparar con docs/05_guia_configuracion.md |

### Errores de Extraccion
| Codigo | Error | Causa | Solucion |
|---|---|---|---|
| ERR-EXT-01 | No se pudo leer el archivo | Archivo corrupto o protegido con contrasena | Verificar que el .xlsx sea valido y no tenga proteccion |
| ERR-EXT-02 | Esquema invalido. Columnas faltantes | El archivo no tiene todas las columnas requeridas | Agregar columnas faltantes al archivo fuente |
| ERR-EXT-03 | Archivo movido a /error | Consecuencia de ERR-EXT-01 o ERR-EXT-02 | Corregir archivo en /error y moverlo de vuelta a /input |

### Errores de Transformacion
| Codigo | Sintoma | Causa | Solucion |
|---|---|---|---|
| ERR-TRF-01 | Fechas como NaT | Formato de fecha no reconocido | Usar formato YYYY-MM-DD |
| ERR-TRF-02 | Valores NaN en Valor_Real | Celdas con texto en columna numerica | Limpiar celdas con texto en el Excel |
| ERR-TRF-03 | Alto numero de registros eliminados | Muchos duplicados o valores invalidos | Revisar calidad del archivo fuente |

### Errores de Exportacion
| Codigo | Error | Causa | Solucion |
|---|---|---|---|
| ERR-EXP-01 | PermissionError al guardar | Archivo de output abierto en Excel | Cerrar el archivo y volver a ejecutar |
| ERR-EXP-02 | Reporte sin datos | JOIN produjo 0 coincidencias | Verificar que ID_Operacion coincida entre fuentes |

## Guia de Diagnostico Rapido

El pipeline no se dispara:
1. Verificar que AMBOS archivos esten en /input
2. Confirmar nombres exactos: source_A.xlsx y source_B.xlsx
3. Revisar logs: logs/etl_YYYY-MM-DD.log

El reporte tiene pocas filas:
1. Comparar ID_Operacion entre source_A y source_B
2. Cambiar tipo de join a "left" en config.yaml si era "inner"
3. Verificar que no haya espacios en blanco en ID_Operacion

## Checklist Pre-Ejecucion
- [ ] config.yaml existe con todas las secciones requeridas
- [ ] Las rutas tienen permisos de lectura/escritura
- [ ] source_A.xlsx tiene: ID_Operacion, Fecha, Unidad, Valor_Real, Responsable
- [ ] source_B.xlsx tiene: ID_Operacion, Periodo, Valor_Meta, Categoria, Estado
- [ ] Los ID_Operacion coinciden entre source_A y source_B
- [ ] Valor_Real mayor a 0 en todos los registros
- [ ] Valor_Meta distinto de 0 en todos los registros
- [ ] Python y dependencias instaladas: pip install -r requirements.txt

*Documento generado automaticamente — Pipeline ETL v1.0.0*

---