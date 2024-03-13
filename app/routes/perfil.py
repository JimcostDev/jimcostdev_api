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
    remove_skill
    
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