from fastapi import APIRouter, Depends, status
from typing import List, Union
from models.work_experience_model import (
    WorkExperienceCreate,
    WorkExperienceResponse
)
from services.work_experience_service import WorkExperienceService
from utils.auth_manager import check_admin_role

router = APIRouter(prefix="/work_experience")
service = WorkExperienceService()

# -- GET públicos con prefijo /p/ --
@router.get(
    "/p/{username}/total_years",
    response_model=int,
    summary="Total de años de experiencia laboral",
    description="Calcula y devuelve el total de años de experiencia laboral de un usuario"
)
async def total_work_years(username: str):
    return await service.get_total_work_experience(username)

@router.get(
    "/p/{username}",
    response_model=List[WorkExperienceResponse],
    summary="Listar experiencias laborales por usuario",
    description="Obtiene todas las experiencias laborales de un usuario por su nombre"
)
async def list_work_experiences(username: str):
    return await service.list_WorkExperience(username)

@router.get(
    "/p/{username}/{id}",
    response_model=WorkExperienceResponse,
    summary="Obtener experiencia laboral por ID y usuario",
    description="Obtiene una experiencia específica de un usuario por su ID"
)
async def get_work_experience(username: str, id: Union[str, int]):
    return await service.get_WorkExperience(id, username)

# -- Operaciones privadas (POST, PUT, DELETE) --
@router.post(
    "/",
    response_model=WorkExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear experiencia laboral",
    description="Crea una experiencia laboral para el usuario autenticado",
)
async def create_work_experience(
    payload: WorkExperienceCreate,
    current_user=Depends(check_admin_role)
):
    return await service.create_WorkExperience(payload, current_user.username)

@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=WorkExperienceResponse,
    summary="Actualizar experiencia laboral",
    description="Actualiza una experiencia laboral existente del usuario autenticado por su ID",
)
async def update_work_experience(
    id: Union[str, int],
    payload: WorkExperienceCreate,
    current_user=Depends(check_admin_role)
):
    return await service.update_WorkExperience(id, payload, current_user.username)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar experiencia laboral",
    description="Elimina una experiencia laboral del usuario autenticado por su ID",
)
async def delete_work_experience(
    id: Union[str, int],
    current_user=Depends(check_admin_role)
):
    await service.delete_WorkExperience(id, current_user.username)
