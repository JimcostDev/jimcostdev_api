# syntax = docker/dockerfile:1.5

########################
# Etapa de construcción
########################
FROM python:3.11-slim AS builder

# Instala dependencias del sistema para compilar extensiones si hiciera falta
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia el fichero de dependencias desde dentro de app/
COPY app/requirements.txt .

# Instala las dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY app ./app

##############################
# Etapa de producción
##############################
FROM python:3.11-slim

WORKDIR /app

# Copia las librerías instaladas en builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copia el código de la aplicación
COPY --from=builder /app/app ./app

# Expone el puerto de FastAPI
EXPOSE 8000

# Arranca FastAPI con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
