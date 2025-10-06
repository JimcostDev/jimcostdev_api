# JimcostDev API

API REST desarrollada con FastAPI para gestionar dinámicamente los datos de mi CV y portafolio profesional. Este backend alimenta tanto mi sitio web personal como la versión descargable de mi currículum.

## 🌐 Ecosistema del Proyecto

Este repositorio forma parte de un ecosistema de 3 aplicaciones:

- **[jimcostdev_api](https://github.com/JimcostDev/jimcostdev_api)** - API REST (FastAPI + MongoDB) ← *Estás aquí*
- **[jimcostdev-astro](https://github.com/JimcostDev/jimcostdev-astro)** - Sitio web principal (Astro + Tailwind CSS)
- **[jimcostdev_cv](https://github.com/JimcostDev/jimcostdev_cv)** - CV descargable (HTML + SCSS + JavaScript)

## 🚀 Tecnologías Utilizadas

[![Python](https://img.shields.io/badge/Python-f6d44e?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-059487?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=101010)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-00Ed64?style=for-the-badge&logo=mongodb&logoColor=white&labelColor=101010)]()

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/JimcostDev/jimcostdev_api.git
cd jimcostdev_api
```

### 2. Crear y activar el entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

**🔄 Actualizar dependencias (opcional):**
```bash
# Reinstalar todas las dependencias
pip uninstall -y -r requirements.txt
pip install -r requirements.txt

# Actualizar un paquete específico
pip install --upgrade nombre-del-paquete
```

### 4. Configurar variables de entorno

Crea un archivo `config.env` dentro de `app/core/`:

```env
MONGO_URI=your_mongodb_connection_uri
JWT_SECRET_KEY=your_secret_key
```

*También puedes exportar estas variables directamente en tu sistema operativo.*

### 5. Configurar la base de datos

Asegúrate de tener MongoDB instalado y crea una base de datos llamada `jimcostdev_api` con las siguientes colecciones:

- `contact`
- `education`
- `perfil`
- `projects`
- `social_networks`
- `work_experience`
- `users`

### 6. Ejecutar el servidor

```bash
cd app
fastapi dev main.py
```

La API estará disponible en `http://localhost:8000`

## 📖 Documentación

Accede a la documentación interactiva de la API:

- **Swagger UI:** `http://localhost:8000/docs`
- **Redoc:** `http://localhost:8000/redoc`

También puedes usar herramientas como **Postman** o **Insomnia** para probar los endpoints.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar algo, abre un **pull request** o crea un **issue**.

## 📜 Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo [LICENSE](./LICENSE) para más detalles.

## 📬 Contacto

Para más información, visita mi sitio web: [jimcostdev.com](https://jimcostdev.com)
