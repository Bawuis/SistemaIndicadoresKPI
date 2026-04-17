"""
Modulo: pipeline.py
Descripcion: Orquestador principal del pipeline ETL.
"""

import os
from datetime import datetime
from loguru import logger

from src.extractor           import leer_y_validar
from src.transformador       import transformar_source_a, transformar_source_b, consolidar
from src.calculador_metricas import calcular_metricas
from src.generador_reporte   import generar_reporte, archivar_fuentes

def ejecutar_pipeline(config: dict) -> None:
    inicio = datetime.now()
    logger.info("=" * 60)
    logger.info("INICIANDO PIPELINE ETL - SistemaIndicadoresKPI")
    logger.info("=" * 60)

    ruta_input = config["rutas"]["input"]
    ruta_error = config["rutas"]["error"]
    llave      = config["join"]["llave_primaria"]
    tipo_join  = config["join"]["tipo"]

    try:
        logger.info("PASO 1: Extraccion y validacion de archivos...")
        cfg_a = config["archivos_esperados"][0]
        cfg_b = config["archivos_esperados"][1]
        df_a_raw = leer_y_validar(os.path.join(ruta_input, cfg_a["nombre"]), cfg_a["columnas_requeridas"], ruta_error)
        df_b_raw = leer_y_validar(os.path.join(ruta_input, cfg_b["nombre"]), cfg_b["columnas_requeridas"], ruta_error)

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
            "Pipeline":               config["pipeline"]["nombre"],
            "Version":                config["pipeline"]["version"],
            "Fecha Ejecucion":        inicio.strftime("%Y-%m-%d"),
            "Hora Inicio":            inicio.strftime("%H:%M:%S"),
            "Hora Fin":               fin.strftime("%H:%M:%S"),
            "Duracion (seg)":         round((fin - inicio).total_seconds(), 2),
            "Registros source_A":     len(df_a),
            "Registros source_B":     len(df_b),
            "Registros Consolidados": len(df_consolidado),
            "Archivo Fuente A":       cfg_a["nombre"],
            "Archivo Fuente B":       cfg_b["nombre"],
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

   
"""
Modulo: monitor.py
Descripcion: Monitor de carpeta de entrada (Event-Driven) usando watchdog.
"""

import time
import os
from loguru import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.config_loader import cargar_configuracion
from src.pipeline import ejecutar_pipeline

class MonitorCarpeta(FileSystemEventHandler):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.ruta_input = config["rutas"]["input"]
        self.archivos_esperados = [a["nombre"] for a in config["archivos_esperados"]]

    def on_created(self, event):
        if event.is_directory:
            return
        nombre_archivo = os.path.basename(event.src_path)
        logger.info(f"Archivo detectado: {nombre_archivo}")
        archivos_presentes = os.listdir(self.ruta_input)
        todos_presentes = all(a in archivos_presentes for a in self.archivos_esperados)
        if todos_presentes:
            logger.success("Todos los archivos detectados. Disparando pipeline ETL...")
            ejecutar_pipeline(self.config)
        else:
            faltantes = [a for a in self.archivos_esperados if a not in archivos_presentes]
            logger.warning(f"Esperando archivos faltantes: {faltantes}")

def iniciar_monitor(ruta_config: str = "config.yaml") -> None:
    config = cargar_configuracion(ruta_config)
    ruta_input = config["rutas"]["input"]
    logger.info(f"Monitoreando carpeta: {ruta_input}")
    event_handler = MonitorCarpeta(config)
    observer = Observer()
    observer.schedule(event_handler, path=ruta_input, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(config["monitoreo"]["intervalo_segundos"])
    except KeyboardInterrupt:
        logger.warning("Monitor detenido manualmente.")
        observer.stop()
    observer.join()