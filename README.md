# JimcostDev API

Este proyecto se encuentra en desarrollo y tiene como objetivo la creación de una API para la gestión de portafolios y currículums (CV). Surge de la necesidad de contar con una página web personal para exhibir mis habilidades y convertir esa información en un formato de CV. Busco encontrar una solución que también pueda ser útil para otras personas.

## Tecnologías Utilizadas

[![Python](https://img.shields.io/badge/Python-f6d44e?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-059487?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=101010)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-00Ed64?style=for-the-badge&logo=mongodb&logoColor=white&labelColor=101010)]()

## Instalación

1. Clona este repositorio ejecutando el siguiente comando:
    ```
    git clone https://github.com/JimcostDev/jimcostdev_api.git
    ```

2. Crea y activa tu entorno virtual:
    - Crea un entorno virtual:
        ```
        python -m venv venv
        ```
    - Activa el entorno virtual:
        - En Windows:
            ```
            venv\Scripts\activate
            ```
        - En macOS y Linux:
            ```
            source venv/bin/activate
            ```

3. Instala las dependencias requeridas:
    ```bash
    pip install -r requirements.txt
    ```
    Instalar dependencias individuales (opcional):
    ```bash
    pip install "fastapi[standard]" motor pymongo pytest pytest-asyncio pydantic-settings aiobcrypt Faker python-jose
    ```

4. Crea un archivo llamado `config.env` dentro de la carpeta `app`. Este archivo se utiliza para cargar las variables de entorno necesarias para la aplicación, como la `JWT_SECRET_KEY` y `MONGO_URI`. El archivo `config.env` debe contener:
    ```plaintext
    MONGO_URI=your_secret_key_here
    JWT_SECRET_KEY=your_secret_key_here
    ```
    
5. Configura la base de datos MongoDB, se llama `jimcostdev_api` con las colecciones `contact`, `education`, `perfil`, `projects`, `social_networks`, `work_experience` y `users` para el correcto funcionamiento de la aplicación.

6. Dirígete al directorio de la aplicación:
    ```
    cd app
    ```

7. Ejecuta la aplicación con el siguiente comando:
    ```
    fastapi dev main.py
    ```
Esta acción iniciará el servidor de desarrollo y podrás acceder a la aplicación desde tu navegador en `http://localhost:8000`.


## Uso y documentación 

1. Accede a `http://localhost:8000/docs` para interactuar con la API y ver la documentación.
2. Utiliza herramientas como Postman o Insomnia para probar los endpoints.

