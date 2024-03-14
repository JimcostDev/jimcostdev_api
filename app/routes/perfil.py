from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.perfil_db import (
    create_perfil,
    add_skill,
    remove_skill,
    get_perfil,
    update_perfil,
    delete_perfil
)
from database.models.perfil_model import PerfilModel, PerfilResponseModel
import logging
from fastapi import status, HTTPException
import logging


logger = logging.getLogger(__name__)
router = APIRouter()

# crear perfil
@router.post(
    "/perfil",
    tags=['perfil'],
    status_code=status.HTTP_201_CREATED,
    summary="Crear perfil",
    description="Crea un nuevo perfil con los datos proporcionados."
)
def create_perfil_endpoint(perfil_data: PerfilModel, current_user: dict = Depends(check_user_role)):
    try:
        created_perfil = create_perfil(perfil_data, username=current_user["username"])
        if created_perfil:
            return created_perfil
    except Exception as ex:
        logger.error(f'ro= Error inesperado al crear perfil: {str(ex)}')
        raise ex
    
# agregar habilidades al perfil
@router.post(
    "/perfil/skill",
    tags=['perfil'],
    status_code=status.HTTP_200_OK,
    summary="Agregar habilidad al perfil",
    description="Agrega una habilidad al perfil del usuario."
)
def add_skill_endpoint(skill: str, current_user: dict = Depends(check_user_role)):
    try:
        added_skill = add_skill(skill, username=current_user["username"])
        if added_skill:
            return added_skill
    except Exception as ex:
        logger.error(f'ro= Error inesperado al agregar habilidad al perfil: {str(ex)}')
        raise ex
    
# remover habilidades del perfil
@router.delete(
    "/perfil/skill",
    tags=['perfil'],
    status_code=status.HTTP_200_OK,
    summary="Remover habilidad del perfil",
    description="Remueve una habilidad del perfil del usuario."
)
def remove_skill_endpoint(skill: str, current_user: dict = Depends(check_user_role)):
    try:
        removed_skill = remove_skill(skill, username=current_user["username"])
        if removed_skill:
            return removed_skill
    except Exception as ex:
        logger.error(f'ro= Error inesperado al remover habilidad del perfil: {str(ex)}')
        raise ex

# obtener perfil
@router.get(
    "/perfil/{username}",
    tags=['perfil'],
    response_model=PerfilResponseModel,
    summary="Obtener perfil",
    description="Obtiene el perfil del usuario."
)
def get_perfil_endpoint(username: str):
    try:
        perfil = get_perfil(username)
        if  perfil is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar la información del usuario, '{username}' no existe.")
        return perfil
    except Exception as ex:
        logger.error(f'ro= Error inesperado al obtener perfil: {str(ex)}')
        raise ex

# actualizar perfil
@router.put(
    "/perfil/{id}",
    tags=['perfil'],
    status_code=status.HTTP_200_OK,
    summary="Actualizar perfil",
    description="Actualiza el perfil del usuario."
)
def update_perfil_endpoint(updated_info: PerfilModel, id: int, current_user: dict = Depends(check_user_role)):
    try:
        username = current_user["username"]
        message  = update_perfil(updated_info, id, username)
        return message
    except Exception as ex:
        logger.error(f'ro= Error inesperado al actualizar perfil: {str(ex)}')
        raise ex


# eliminar perfil
@router.delete(
    "/perfil/{id}",
    tags=['perfil'],
    status_code=status.HTTP_200_OK,
    summary="Eliminar perfil",
    description="Elimina el perfil del usuario."
)
def delete_perfil_endpoint(id: int, current_user: dict = Depends(check_user_role)):
    try:
        username = current_user["username"]
        message  = delete_perfil(id, username)
        if message:
            return message
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se pudo encontrar la información de perfil, el usuario '{username}' no existe o no tiene información asociada al id proporcionado."
            )
    except Exception as ex:
        logger.error(f'ro= Error inesperado al eliminar perfil: {str(ex)}')
        raise ex