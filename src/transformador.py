"""
Modulo: transformador.py
Descripcion: Limpieza, normalizacion y consolidacion (JOIN) de los DataFrames.
"""

import pandas as pd
from loguru import logger

def transformar_source_a(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando source_A...")
    df = df.copy()
    df["Fecha"]      = pd.to_datetime(df["Fecha"], errors="coerce")
    df["Valor_Real"] = pd.to_numeric(df["Valor_Real"], errors="coerce")
    antes = len(df)
    df = df.drop_duplicates(subset=["ID_Operacion"])
    logger.debug(f"Duplicados eliminados en source_A: {antes - len(df)}")
    df = df[df["Valor_Real"] > 0]
    df = df.dropna(subset=["ID_Operacion", "Fecha", "Valor_Real"])
    logger.success(f"source_A transformado: {len(df)} registros validos.")
    return df.reset_index(drop=True)

def transformar_source_b(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando source_B...")
    df = df.copy()
    df["Valor_Meta"] = pd.to_numeric(df["Valor_Meta"], errors="coerce")
    df = df.dropna(subset=["ID_Operacion", "Valor_Meta"])
    df = df.drop_duplicates(subset=["ID_Operacion"])
    logger.success(f"source_B transformado: {len(df)} registros validos.")
    return df.reset_index(drop=True)

def consolidar(df_a: pd.DataFrame, df_b: pd.DataFrame, llave: str, tipo_join: str = "left") -> pd.DataFrame:
    logger.info(f"Consolidando tablas con JOIN '{tipo_join}' por '{llave}'...")
    df_consolidado = pd.merge(df_a, df_b, on=llave, how=tipo_join)
    logger.success(f"Consolidacion completada: {len(df_consolidado)} registros resultantes.")
    return df_consolidado