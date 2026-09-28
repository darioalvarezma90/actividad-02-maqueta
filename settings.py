from pathlib import Path
import os

# Esto asegura que las rutas funcionen tanto en tu PC como en el contenedor de Linux
BASE_DIR = Path(__file__).resolve().parent

# Puerto configurable para ejecución local, Koyeb y Cloud Run.
PORT = int(os.environ.get("PORT", 8080))
HOST = "0.0.0.0"
LOG_LEVEL = "info"
