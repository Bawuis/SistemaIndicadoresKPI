"""
Punto de entrada principal del sistema ETL - SistemaIndicadoresKPI
Uso:
    python main.py             # Inicia monitor continuo (Event-Driven)
    python main.py --once      # Ejecuta el pipeline una sola vez
"""

import argparse
from loguru import logger
from src.config_loader import cargar_configuracion, crear_directorios
from src.monitor       import iniciar_monitor
from src.pipeline      import ejecutar_pipeline

def configurar_logs(config: dict) -> None:
    import os
    ruta_logs = config["rutas"]["logs"]
    os.makedirs(ruta_logs, exist_ok=True)
    logger.add(
        f"{ruta_logs}/etl_{{time:YYYY-MM-DD}}.log",
        rotation="00:00",
        retention="30 days",
        level="INFO",
        encoding="utf-8"
    )

def main():
    parser = argparse.ArgumentParser(description="SistemaIndicadoresKPI - Pipeline ETL")
    parser.add_argument("--once", action="store_true", help="Ejecuta el pipeline una sola vez")
    args = parser.parse_args()
    config = cargar_configuracion("config.yaml")
    crear_directorios(config)
    configurar_logs(config)
    if args.once:
        logger.info("Modo: Ejecucion unica")
        ejecutar_pipeline(config)
    else:
        logger.info("Modo: Monitor continuo (Event-Driven)")
        iniciar_monitor("config.yaml")

if __name__ == "__main__":
    main()