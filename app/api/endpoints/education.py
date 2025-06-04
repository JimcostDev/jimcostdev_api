from fastapi import APIRouter, Depends, status
from models.education_model import (
    EducationCreate,
    EducationResponse
)
from services.education_service import EducationService
from utils.auth_manager import check_admin_role

router = APIRouter(prefix="/education")
service = EducationService()

# -- GET públicos con prefijo /p/ --
@router.get(
    "/p/{username}",
    response_model=list[EducationResponse],
    summary="Listar datos de educación por usuario",
    description="Obtiene todas los datos de educación de un usuario por su nombre"
)
async def list_education(username: str):
    return await service.list_education(username)

@router.get(
    "/p/{username}/{id}",
    response_model=EducationResponse,
    summary="Obtener educación por ID y usuario",
    description="Obtiene una educación específica de un usuario por su ID"
)
async def get_education(username: str, id: str):
    return await service.get_education(id, username)


# -- Operaciones privadas (POST, PUT, DELETE) --
@router.post(
    "/",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear educación",
    description="Crea educación para el usuario autenticado",
)
async def create_education(
    payload: EducationCreate,
    current_user=Depends(check_admin_role)
):
    return await service.create_education(payload, current_user.username)

@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=EducationResponse,
    summary="Actualizar educación",
    description="Actualiza educación existente del usuario autenticado por su ID",
)
async def update_education(
    id: str,
    payload: EducationCreate,
    current_user=Depends(check_admin_role)
):
    return await service.update_education(id, payload, current_user.username)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar educación",
    description="Elimina educación del usuario autenticado por su ID",
)
async def delete_education(
    id: str,
    current_user=Depends(check_admin_role)
):
    await service.delete_education(id, current_user.username)