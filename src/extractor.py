"""
Modulo: extractor.py
Descripcion: Extraccion y validacion de esquema de los archivos Excel de entrada.
"""

import pandas as pd
import shutil
import os
from loguru import logger

def leer_y_validar(ruta_archivo: str, columnas_requeridas: list, ruta_error: str) -> pd.DataFrame:
    logger.info(f"Leyendo archivo: {ruta_archivo}")
    try:
        df = pd.read_excel(ruta_archivo, engine="openpyxl")
    except Exception as e:
        logger.error(f"No se pudo leer el archivo {ruta_archivo}: {e}")
        _mover_a_error(ruta_archivo, ruta_error)
        raise
    columnas_faltantes = [c for c in columnas_requeridas if c not in df.columns]
    if columnas_faltantes:
        logger.error(f"Columnas faltantes en {ruta_archivo}: {columnas_faltantes}")
        _mover_a_error(ruta_archivo, ruta_error)
        raise ValueError(f"Esquema invalido. Columnas faltantes: {columnas_faltantes}")
    logger.success(f"Archivo validado correctamente: {os.path.basename(ruta_archivo)}")
    return df

def _mover_a_error(ruta_origen: str, ruta_error: str) -> None:
    os.makedirs(ruta_error, exist_ok=True)
    nombre = os.path.basename(ruta_origen)
    destino = os.path.join(ruta_error, nombre)
    shutil.move(ruta_origen, destino)
    logger.warning(f"Archivo movido a /error: {destino}")