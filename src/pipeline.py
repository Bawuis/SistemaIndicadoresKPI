"""
Modulo: pipeline.py
Descripcion: Orquestador principal del pipeline ETL.
"""

import os
from datetime import datetime
from loguru import logger

from src.extractor import leer_y_validar
from src.transformador import transformar_source_a, transformar_source_b, consolidar
from src.calculador_metricas import calcular_metricas
from src.generador_reporte import generar_reporte, archivar_fuentes


def ejecutar_pipeline(config: dict) -> None:
    inicio = datetime.now()
    logger.info("=" * 60)
    logger.info("INICIANDO PIPELINE ETL - SistemaIndicadoresKPI")
    logger.info("=" * 60)

    ruta_input = config["rutas"]["input"]
    ruta_error = config["rutas"]["error"]
    llave = config["join"]["llave_primaria"]
    tipo_join = config["join"]["tipo"]

    try:
        logger.info("PASO 1: Extraccion y validacion de archivos...")
        cfg_a = config["archivos_esperados"][0]
        cfg_b = config["archivos_esperados"][1]
        df_a_raw = leer_y_validar(
            os.path.join(ruta_input, cfg_a["nombre"]), cfg_a["columnas_requeridas"], ruta_error
        )
        df_b_raw = leer_y_validar(
            os.path.join(ruta_input, cfg_b["nombre"]), cfg_b["columnas_requeridas"], ruta_error
        )

        logger.info("PASO 2: Transformacion y limpieza de datos...")
        df_a = transformar_source_a(df_a_raw)
        df_b = transformar_source_b(df_b_raw)

        logger.info("PASO 3: Consolidacion de fuentes (JOIN)...")
        df_consolidado = consolidar(df_a, df_b, llave=llave, tipo_join=tipo_join)

        logger.info("PASO 4: Calculo de metricas de desempeno...")
        df_detalle, df_resumen = calcular_metricas(df_consolidado, config)

        logger.info("PASO 5: Generacion del reporte Excel...")
        fin = datetime.now()
        metadata = {
            "Pipeline": config["pipeline"]["nombre"],
            "Version": config["pipeline"]["version"],
            "Fecha Ejecucion": inicio.strftime("%Y-%m-%d"),
            "Hora Inicio": inicio.strftime("%H:%M:%S"),
            "Hora Fin": fin.strftime("%H:%M:%S"),
            "Duracion (seg)": round((fin - inicio).total_seconds(), 2),
            "Registros source_A": len(df_a),
            "Registros source_B": len(df_b),
            "Registros Consolidados": len(df_consolidado),
            "Archivo Fuente A": cfg_a["nombre"],
            "Archivo Fuente B": cfg_b["nombre"],
        }
        ruta_reporte = generar_reporte(df_detalle, df_resumen, config, metadata)

        logger.info("PASO 6: Archivando fuentes procesadas...")
        archivar_fuentes(config)

        logger.info("=" * 60)
        logger.success(f"PIPELINE COMPLETADO en {metadata['Duracion (seg)']}s")
        logger.success(f"Reporte: {ruta_reporte}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"ERROR en el pipeline: {e}")
        raise
