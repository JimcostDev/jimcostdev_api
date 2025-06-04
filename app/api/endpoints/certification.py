from fastapi import APIRouter, Depends, status
from models.certification_model import (
    CertificationCreate,
    CertificationResponse
)
from services.certification_service import CertificationService
from utils.auth_manager import check_admin_role

router = APIRouter(prefix="/certifications")
service = CertificationService()

# -- GET públicos con prefijo /p/ --
@router.get(
    "/p/{username}",
    response_model=list[CertificationResponse],
    summary="Listar certificaciones por usuario",
    description="Obtiene todas las certificaciones de un usuario por su nombre"
)
async def list_certifications(username: str):
    return await service.list_certifications(username)

@router.get(
    "/p/{username}/{id}",
    response_model=CertificationResponse,
    summary="Obtener certificación por ID y usuario",
    description="Obtiene una certificación específica de un usuario por su ID"
)
async def get_certification(username: str, id: str):
    return await service.get_certification(id, username)
    

# -- Operaciones privadas (POST, PUT, DELETE) --
@router.post(
    "/",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear certificación",
    description="Crea una nueva certificación para el usuario autenticado",
)
async def create_certification(
    payload: CertificationCreate,
    current_user=Depends(check_admin_role)
):
    return await service.create_certification(payload, current_user.username)
    
    

@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CertificationResponse,
    summary="Actualizar certificación",
    description="Actualiza una certificación existente del usuario autenticado por su ID",
)
async def update_certification(
    id: str,
    payload: CertificationCreate,
    current_user=Depends(check_admin_role)
):
    return await service.update_certification(id, payload, current_user.username)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar certificación",
    description="Elimina una certificación del usuario autenticado por su ID",
)
async def delete_certification(
    id: str,
    current_user=Depends(check_admin_role)
):
    await service.delete_certification(id, current_user.username)
  
    
    