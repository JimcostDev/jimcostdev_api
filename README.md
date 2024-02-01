# JimcostDev API

Este proyecto se encuentra en desarrollo y tiene como objetivo la creación de una API para la gestión de portafolios y currículums (CV). Surge de la necesidad de contar con una página web personal para exhibir mis habilidades y también convertir esa información en un formato de CV. Busco encontrar una solución que pueda ser útil para otras personas.

## Tecnologías Utilizadas

[![Python](https://img.shields.io/badge/Python-1f425f?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)]()

[![FastAPI](https://img.shields.io/badge/FastAPI-00599C?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=101010)](https://fastapi.tiangolo.com/)

[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white&labelColor=101010)]()

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
    ```
    pip install -r requirements.txt
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
    uvicorn main:app --reload
    ```
Esta acción iniciará el servidor de desarrollo y podrás acceder a la aplicación desde tu navegador en `http://localhost:8000`.


## Uso y documentación 

1. Accede a `http://localhost:8000/docs` para interactuar con la API y ver la documentación.
2. Utiliza herramientas como Postman o Insomnia para probar los endpoints.

## Contribución

¡Gracias por considerar contribuir a este proyecto! Si deseas agregar nuevas características, solucionar problemas existentes o mejorar la aplicación de alguna manera, aquí hay algunos pasos para comenzar:

1. Haz un fork del repositorio a través del botón de "Fork" en la parte superior derecha de esta página.
   
2. Clona tu repositorio forkeado:
    ```bash
    git clone https://github.com/TU_USUARIO/nombre-del-repositorio.git
    ```

3. Crea una nueva rama para trabajar en tu característica:
    ```bash
    git checkout -b feature/nueva-caracteristica
    ```

4. Realiza los cambios necesarios y añade tus contribuciones:
    ```bash
    git add .
    git commit -m 'Agrega nueva característica'
    ```

5. Sube tus cambios a tu repositorio en GitHub:
    ```bash
    git push origin feature/nueva-caracteristica
    ```

6. Abre un Pull Request desde tu rama a la rama principal de este repositorio.
   
Una vez abierto, tu Pull Request será revisado y, si todo está correcto, será fusionado. ¡Gracias por tu contribución!
