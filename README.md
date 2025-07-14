# JimcostDev API

API desarrollada con FastAPI para administrar de manera eficiente mi CV y portafolio profesional. Este proyecto surgió de la necesidad de contar con una página web personal para exhibir habilidades profesionales y generar un CV de manera automática.

## Tecnologías Utilizadas

[![Python](https://img.shields.io/badge/Python-f6d44e?style=for-the-badge\&logo=python\&logoColor=white\&labelColor=101010)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-059487?style=for-the-badge\&logo=fastapi\&logoColor=white\&labelColor=101010)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-00Ed64?style=for-the-badge\&logo=mongodb\&logoColor=white\&labelColor=101010)]()

## Instalación

Sigue los siguientes pasos para instalar y ejecutar el proyecto localmente:

1. **Clona este repositorio:**

   ```bash
   git clone https://github.com/JimcostDev/jimcostdev_api.git
   ```

2. **Crea y activa un entorno virtual:**

   * En Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * En macOS o Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

   **🔄 Actualización de dependencias (opcional)**
   Si deseas actualizar todas las dependencias desde cero:

   ```bash
   pip uninstall -y -r requirements.txt
   pip install -r requirements.txt
   ```
   También puedes actualizar paquetes de forma individual: 
   ```bash
   pip install --upgrade nombre-del-paquete
   ```
4. **Configura las variables de entorno:**
   Crea un archivo `config.env` dentro de la carpeta `app/core/` con el siguiente contenido:

   ```dotenv
   MONGO_URI=your_mongodb_connection_uri
   JWT_SECRET_KEY=your_secret_key
   ```

   *Alternativamente, puedes exportar estas variables desde tu sistema operativo.*

5. **Configura la base de datos:**
   Asegúrate de tener una base de datos llamada `jimcostdev_api` con las siguientes colecciones:

   * `contact`
   * `education`
   * `perfil`
   * `projects`
   * `social_networks`
   * `work_experience`
   * `users`

6. **Dirígete al directorio de la aplicación:**

   ```bash
   cd app
   ```

7. **Ejecuta el servidor de desarrollo:**

   ```bash
   fastapi dev main.py
   ```

Una vez iniciado, puedes acceder a la aplicación en tu navegador a través de `http://localhost:8000`.

## Uso y Documentación

* Accede a la documentación interactiva de la API en:

  * `http://localhost:8000/docs` (Swagger UI)
  * `http://localhost:8000/redoc` (Redoc)

* También puedes utilizar herramientas como **Postman** o **Insomnia** para probar los endpoints de la API.

---

