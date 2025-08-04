# syntax = docker/dockerfile:1.5

########################
# Etapa de construcción
########################
FROM python:3.11-slim AS builder

# Instala build-essential si tus dependencias nativas lo requieren
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia y instala dependencias
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la aplicación
COPY app/ .

##############################
# Etapa de producción
##############################
FROM python:3.11-slim

WORKDIR /app

# Copia los paquetes instalados y tu código
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app .

# Expone el puerto de FastAPI
EXPOSE 8000

# Usa python -m uvicorn para que siempre exista el punto de entrada
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
