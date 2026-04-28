"""
Modulo: monitor.py
Descripcion: Monitor de carpeta de entrada (Event-Driven) usando watchdog.
"""

import os
import time
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

    def _intentar_ejecucion(self) -> None:
        archivos_presentes = os.listdir(self.ruta_input)
        todos_presentes = all(a in archivos_presentes for a in self.archivos_esperados)

        if todos_presentes:
            logger.success("Todos los archivos detectados. Disparando pipeline ETL...")
            ejecutar_pipeline(self.config)
        else:
            faltantes = [a for a in self.archivos_esperados if a not in archivos_presentes]
            logger.warning(f"Esperando archivos faltantes: {faltantes}")

    def on_created(self, event):
        if event.is_directory:
            return

        nombre_archivo = os.path.basename(event.src_path)
        logger.info(f"Archivo detectado: {nombre_archivo}")
        self._intentar_ejecucion()

    def on_moved(self, event):
        if event.is_directory:
            return

        nombre_archivo = os.path.basename(event.dest_path)
        logger.info(f"Archivo movido/detectado: {nombre_archivo}")
        self._intentar_ejecucion()


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
