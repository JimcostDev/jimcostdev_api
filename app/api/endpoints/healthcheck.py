from fastapi import APIRouter
from core.config import settings
from core.database import mongodb

router = APIRouter()

@router.get(
    "/healthcheck",
    include_in_schema=False,
    summary="Verificación de salud del sistema",
    description="Proporciona el estado actual del servicio y sus dependencias"
)
async def health_check():
    service_status = {
        "status": "healthy",
        "version": settings.PROJECT_VERSION,
        "dependencies": {
            "database": "healthy"
        }
    }

    # Verificación de la base de datos
    if mongodb.client:
        try:
            await mongodb.client.admin.command("ping")
        except Exception as e:
            service_status["dependencies"]["database"] = f"unhealthy: {str(e)}"
            service_status["status"] = "degraded"
    else:
        service_status["dependencies"]["database"] = "disconnected"
        service_status["status"] = "degraded"

    return service_status
