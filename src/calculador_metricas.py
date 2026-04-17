"""
Modulo: calculador_metricas.py
Descripcion: Calculo de metricas de desempeno sobre el DataFrame consolidado.
"""

import pandas as pd
from loguru import logger

def calcular_metricas(df: pd.DataFrame, config: dict) -> tuple:
    logger.info("Calculando metricas de desempeno...")
    umbral_optimo    = config["metricas"]["cumplimiento_optimo"]
    umbral_en_riesgo = config["metricas"]["cumplimiento_en_riesgo"]
    df = df.copy()

    # METRICA 1: % de Cumplimiento
    df["Pct_Cumplimiento"] = df.apply(
        lambda row: round((row["Valor_Real"] / row["Valor_Meta"]) * 100, 2)
        if pd.notna(row["Valor_Meta"]) and row["Valor_Meta"] != 0 else None,
        axis=1
    )

    # METRICA 2: Variacion Absoluta
    df["Variacion_Abs"] = df["Valor_Real"] - df["Valor_Meta"]

    # METRICA 3: Semaforo
    def semaforo(pct):
        if pd.isna(pct):       return "Sin Datos"
        elif pct >= umbral_optimo:    return "Optimo"
        elif pct >= umbral_en_riesgo: return "En Riesgo"
        else:                         return "Critico"

    df["Semaforo"] = df["Pct_Cumplimiento"].apply(semaforo)

    resumen = pd.DataFrame([
        {"Metrica": "Promedio Cumplimiento (%)",   "Valor": round(df["Pct_Cumplimiento"].mean(), 2)},
        {"Metrica": "Total Valor Real",             "Valor": round(df["Valor_Real"].sum(), 2)},
        {"Metrica": "Total Valor Meta",             "Valor": round(df["Valor_Meta"].sum(), 2)},
        {"Metrica": "Operaciones Optimas",          "Valor": (df["Semaforo"] == "Optimo").sum()},
        {"Metrica": "Operaciones En Riesgo",        "Valor": (df["Semaforo"] == "En Riesgo").sum()},
        {"Metrica": "Operaciones Criticas",         "Valor": (df["Semaforo"] == "Critico").sum()},
        {"Metrica": "Total Operaciones",            "Valor": len(df)},
    ])

    logger.success("Metricas calculadas correctamente.")
    return df, resumen