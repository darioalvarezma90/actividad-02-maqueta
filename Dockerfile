# Usa la imagen oficial y ligera de Python
FROM python:3.11-slim

# Crea el directorio de trabajo
WORKDIR /app

# Copia los requerimientos y las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente al contenedor (incluyendo carpetas assets y templates)
COPY . .

# Expone el puerto que usará Cloud Run (8080 por defecto)
EXPOSE 8080

# Inicia la aplicación usando Uvicorn (adaptando el puerto mediante variable de entorno)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]