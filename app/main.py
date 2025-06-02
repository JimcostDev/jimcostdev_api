from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import mongodb 
from api.endpoints.healthcheck import router as healthcheck_router
from api.endpoints.user  import router as user_router
from api.endpoints.auth  import router as auth_router
from api.endpoints.social_network import router as social_network_router
from api.endpoints.certification import router as certification_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización de la conexión a MongoDB
    try:
        await mongodb.connect()
        print("✅ Conexión a MongoDB establecida correctamente")
    except Exception as e:
        print(f"❌ Error fatal de conexión a MongoDB: {str(e)}")
        raise RuntimeError("No se pudo iniciar la aplicación - Error de base de datos") from e
        
    yield  # La aplicación se ejecuta aquí
        
    # Cierre de la conexión al finalizar
    await mongodb.disconnect()
    print("🔌 Conexión a MongoDB cerrada")

app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(healthcheck_router, prefix=settings.API_PREFIX, tags=["healthcheck"])
app.include_router(auth_router,  prefix=settings.API_PREFIX, tags=["auth"])
app.include_router(user_router,  prefix=settings.API_PREFIX, tags=["users"])
app.include_router(social_network_router, prefix=settings.API_PREFIX, tags=["social_networks"])
app.include_router(certification_router, prefix=settings.API_PREFIX, tags=["certifications"])

# Archivos estáticos
app.mount("/static", StaticFiles(directory="assets"), name="static")

