"""
Modulo: config_loader.py
Descripcion: Carga y valida la configuracion del pipeline desde config.yaml
"""

import yaml
import os
from loguru import logger

def cargar_configuracion(ruta_config: str = "config.yaml") -> dict:
    if not os.path.exists(ruta_config):
        logger.error(f"Archivo de configuracion no encontrado: {ruta_config}")
        raise FileNotFoundError(f"No se encontro: {ruta_config}")
    with open(ruta_config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    logger.info(f"Configuracion cargada correctamente desde: {ruta_config}")
    return config

def crear_directorios(config: dict) -> None:
    rutas = config.get("rutas", {})
    for nombre, ruta in rutas.items():
        os.makedirs(ruta, exist_ok=True)
        logger.debug(f"Directorio verificado/creado: {ruta}")