# Imagen base oficial de Python
FROM python:3.12-slim

# Directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias desde la carpeta app/
COPY app/requirements.txt .

# Instala las dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo el código de la aplicación desde la carpeta app/
COPY app/ .

# Expone el puerto 8000 (puerto por defecto de FastAPI)
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]