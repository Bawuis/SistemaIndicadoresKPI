"""
Modulo: monitor.py
Descripcion: Monitor de carpeta de entrada (Event-Driven) usando watchdog.
"""

import os
import time
import unicodedata
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
        cfg_excel = config.get("consolidacion_excel", {})
        self.keywords = [
            cfg_excel.get("keyword_elearning", "elearning"),
            cfg_excel.get("keyword_files_jmc", "filesjmc"),
            cfg_excel.get("keyword_participantes", "participantes"),
        ]

    @staticmethod
    def _normalizar(nombre: str) -> str:
        texto = str(nombre).strip().lower()
        texto = "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")
        return "".join(c for c in texto if c.isalnum())

    def _intentar_ejecucion(self) -> None:
        archivos_presentes = [
            f for f in os.listdir(self.ruta_input) if not f.startswith("~$") and f.lower().endswith((".xlsx", ".xlsm", ".xls"))
        ]
        archivos_norm = [self._normalizar(f) for f in archivos_presentes]

        faltantes = []
        for kw in self.keywords:
            kw_norm = self._normalizar(kw)
            if not any(kw_norm in nombre for nombre in archivos_norm):
                faltantes.append(kw)

        todos_presentes = len(faltantes) == 0

        if todos_presentes:
            logger.success("Todos los archivos detectados. Disparando pipeline ETL...")
            ejecutar_pipeline(self.config)
        else:
            logger.warning(f"Esperando archivos faltantes por keyword: {faltantes}")

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
