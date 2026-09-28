"""Configuración compartida entre la ejecución local y Docker."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
# La ruta no depende del directorio desde el que se inicia el proceso.
# Las variables del sistema o del contenedor tienen prioridad sobre el archivo.
load_dotenv(BASE_DIR / ".env", override=False, encoding="utf-8-sig")

HOST = os.getenv("APP_HOST", "127.0.0.1")
try:
    PORT = int(os.getenv("APP_PORT", "8000"))
except ValueError as exc:
    raise ValueError("APP_PORT debe ser un número entero entre 1 y 65535.") from exc
if not 1 <= PORT <= 65535:
    raise ValueError("APP_PORT debe ser un número entero entre 1 y 65535.")

LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "info").lower()
if LOG_LEVEL not in {"critical", "error", "warning", "info", "debug", "trace"}:
    raise ValueError("APP_LOG_LEVEL debe ser critical, error, warning, info, debug o trace.")
