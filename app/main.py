from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI(
    title="JimcostDev API",
    description="Bienvenido a la API de Mi Portafolio, diseñada para gestionar información sobre mi perfil, proyectos y más.",
    version="0.1.0",
)

# Configurar CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jimcostdev.github.io",
                   "https://jimcostdev.com",
                   "https://cv.jimcostdev.com",
                   "https://jimcostdev-astro.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# incluir el favicon
app.mount("/favicon.ico", StaticFiles(directory="assets"), name="favicon")

# Ruta de healthcheck
@app.get("/healthcheck", tags=["healthcheck"])
async def healthcheck():
    return {"status": "OK"}

# Función para cargar rutas dinámicamente
def load_routes(app):
    routes_directory = Path(__file__).parent / "routes"

    for route_file in routes_directory.glob("*.py"):
        if route_file.name != "__init__.py":
            module = __import__(f"routes.{route_file.stem}", fromlist=["router"])
            app.include_router(module.router)

# Cargar rutas
load_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)