FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 10001 app
COPY main.py settings.py ./
COPY templates/ ./templates/
COPY public/ ./public/
USER app

EXPOSE 8080

# main.py utiliza PORT, compatible con Koyeb y Cloud Run.
CMD ["python", "main.py"]
