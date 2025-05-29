from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import mongodb 
from api.endpoints.hello import router as hello_router
from api.endpoints.user  import router as user_router
from api.endpoints.auth  import router as auth_router
from api.endpoints.social_network import router as social_network_router

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
app.include_router(hello_router, prefix=settings.API_PREFIX, tags=["hello"])
app.include_router(user_router,  prefix=settings.API_PREFIX, tags=["users"])
app.include_router(auth_router,  prefix=settings.API_PREFIX, tags=["auth"])
app.include_router(social_network_router, prefix=settings.API_PREFIX, tags=["social_networks"])

# Archivos estáticos
app.mount("/static", StaticFiles(directory="assets"), name="static")

# Endpoint de verificación de salud mejorado
@app.get(
    "/ok",
    include_in_schema=False,
    summary="Verificación de salud del sistema",
    description="Proporciona el estado actual del servicio y sus dependencias"
)
async def health_check():
    service_status = {
        "status": "running",
        "version": settings.PROJECT_VERSION,
        "dependencies": {
            "database": "disconnected"
        }
    }
    
    # Verificación de la base de datos
    if mongodb.client:
        try:
            await mongodb.client.admin.command('ping')
            service_status["dependencies"]["database"] = "healthy"
        except Exception as e:
            service_status["dependencies"]["database"] = f"unhealthy: {str(e)}"
    
    return service_status