from fastapi import APIRouter
from core.config import settings
from core.database import mongodb 

router = APIRouter()

# Endpoint de verificación de salud mejorado
@router.get(
    "/healthcheck",
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