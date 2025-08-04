# syntax=docker/dockerfile:1.5

##############################
# Etapa única: build + runtime
##############################
FROM python:3.11-slim

# 1) Instala herramientas de compilación (solo si haces extensiones nativas)
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Copia las dependencias y las instala
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copia el código de tu FastAPI
COPY app ./app

# 4) Expone el puerto en el que correrá Uvicorn
EXPOSE 8000

# 5) Arranca tu API con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
