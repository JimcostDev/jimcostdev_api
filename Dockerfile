# syntax=docker/dockerfile:1

########################
# 1) Builder: compila ruedas (wheels)
########################
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Dependencias necesarias para compilar paquetes con extensiones nativas
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    python3-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (mejor cache)
COPY app/requirements.txt .

# Precompilar ruedas para acelerar instalación en el runtime
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip wheel -r requirements.txt -w /wheels

########################
# 2) Runtime: imagen final ligera
########################
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

WORKDIR /app

# Librerías del sistema necesarias en tiempo de ejecución (ajusta según tu app)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    libpq5 \
 && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN useradd --create-home --shell /bin/bash appuser

# Copiar ruedas y requirements desde el builder
COPY --from=builder /wheels /wheels
COPY app/requirements.txt .

# Instalar dependencias desde las ruedas (sin recompilar)
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir --find-links /wheels -r requirements.txt \
 && rm -rf /wheels

# Copiar el código de la aplicación
COPY app/ .

# Ejecutar el contenedor como usuario no-root
USER appuser

EXPOSE 8000

# Healthcheck alineado con tu endpoint FastAPI
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://127.0.0.1:8000/healthcheck || exit 1

# Producción recomendado (Gunicorn + Uvicorn workers):
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000", "--workers", "4", "--log-level", "info"]

# Por defecto: Uvicorn (más simple, útil en desarrollo)
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
