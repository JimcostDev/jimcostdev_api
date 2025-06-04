from fastapi import APIRouter, Body, Depends, status
from models.profile_model import (
    ProfileCreate,
    ProfileResponse
)
from services.profile_service import ProfileService
from utils.auth_manager import check_admin_role

router = APIRouter(prefix="/profile")
service = ProfileService()

# -- GET públicos con prefijo /p/ --
@router.get(
    "/p/{username}",
    response_model=list[ProfileResponse],
    summary="Obtner perfil de usuario",
    description="Obtiene el perfil de un usuario por su nombre"
)
async def list_profiles(username: str):
    return await service.list_profiles(username)

# -- Operaciones privadas (POST, PUT, DELETE) --
@router.post(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear perfil",
    description="Crear perfil para el usuario autenticado",
)
async def create_profile(
    payload: ProfileCreate,
    current_user=Depends(check_admin_role)
):
    return await service.create_profile(payload, current_user.username)
    
    

@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfileResponse,
    summary="Actualizar perfil",
    description="Actualiza perfil existente del usuario autenticado por su ID",
)
async def update_profile(
    id: str,
    payload: ProfileCreate,
    current_user=Depends(check_admin_role)
):
    return await service.update_profile(id, payload, current_user.username)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar perfil",
    description="Elimina perfil del usuario autenticado por su ID",
)
async def delete_profile(
    id: str,
    current_user=Depends(check_admin_role)
):
    await service.delete_profile(id, current_user.username)
    
# -- Nuevos endpoints para habilidades --
@router.post(
    "/skill",
    status_code=status.HTTP_200_OK,
    summary="Agregar habilidad",
    description="Agrega una habilidad al perfil del usuario autenticado"
)
async def add_skill(
    skill: str = Body(..., embed=True, description="Nombre de la habilidad a agregar"),
    current_user=Depends(check_admin_role)
):
    """
    Cuerpo de ejemplo:
    {
      "skill": "python"
    }
    """
    return await service.add_skill(skill, current_user.username)


@router.delete(
    "/skill/{skill}",
    status_code=status.HTTP_200_OK,
    summary="Remover habilidad",
    description="Elimina una habilidad del perfil del usuario autenticado"
)
async def remove_skill(
    skill: str,
    current_user=Depends(check_admin_role)
) :
    """
    Llama a service.remove_skill(skill, username).
    """
    return await service.remove_skill(skill, current_user.username)
  
    
    