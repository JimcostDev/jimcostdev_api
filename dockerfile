# syntax = docker/dockerfile:1.5

########################
# Etapa de construcción
########################
FROM python:3.11-slim AS builder

# Instala build-essential si necesitas compilar dependencias nativas
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) Copia el requirements.txt que está dentro de app/
COPY app/requirements.txt .

# 2) Instala las dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copia TODO el contenido de app/ directamente en /app
COPY app/ .

##############################
# Etapa de producción
##############################
FROM python:3.11-slim

WORKDIR /app

# Copia las librerías instaladas en builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copia el código (core/, routes/, main.py, etc.)
COPY --from=builder /app .

# Expone el puerto de FastAPI
EXPOSE 8000

# Arranca FastAPI con Uvicorn apuntando al main.py de la raíz
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
