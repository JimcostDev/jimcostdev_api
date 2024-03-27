from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.work_experience_db import (
    get_work_experiences_by_user,
    create_work_experience,
    update_work_experience,
    delete_work_experience,
    get_total_work_experience
)
from database.models.work_experience_model import WorkExperienceModel, WorkExperienceResponseModel
import logging
from fastapi import status, HTTPException
import logging


logger = logging.getLogger(__name__)
router = APIRouter()

# obtener experiencia laboral por usuario
@router.get(
    "/work_experience/{username}",
    tags=['work_experience'],
    response_model=List[WorkExperienceResponseModel],
    summary="Obtener toda la experiencia laboralcde un usuario",
    description="Este endpoint permite obtener toda la experiencia laboral de un usuario"
)
def get_work_experiences_endpoint(username: str):
    try:
        work_experiences = get_work_experiences_by_user(username)

        if work_experiences == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar la experiencia laboral para el usuario, '{username}'")
        return work_experiences
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al obtener la experiencia laboral: {str(ex)}')
        raise ex

# crear una nueva experiencia laboral
@router.post(
    "/work_experience",
    tags=['work_experience'],
    status_code=status.HTTP_201_CREATED,
    summary="Crear experiencia laboral",
    description="Crea un nueva experiencia laboral con los datos proporcionados."
)
def create_work_experience_endpoint(work_experience_data: WorkExperienceModel, current_user: dict = Depends(check_user_role)):
    try:
        created_work_experience = create_work_experience(work_experience_data, username=current_user["username"])
        if created_work_experience:
            return created_work_experience
    except Exception as ex:
        logger.error(f'ro= Error inesperado al crear experiencia laboral: {str(ex)}')
        raise ex

# actualizar experiencia laboral
@router.put(
    "/work_experience/{id}",
    tags=['work_experience'],
    status_code=status.HTTP_200_OK,
    summary="Actualizar experiencia laboral",
    description="Actualiza la experiencia laboral del usuario."
)
def update_work_experience_endpoint(updated_info: WorkExperienceModel, id: int, current_user: dict = Depends(check_user_role)):
    try:
        username = current_user["username"]
        message  = update_work_experience(updated_info, id, username)
        return message
    except Exception as ex:
        logger.error(f'ro= Error inesperado al actualizar la experiencia laboral: {str(ex)}')
        raise ex


# eliminar experiencia laboral
@router.delete(
    "/work_experience/{id}",
    tags=['work_experience'],
    status_code=status.HTTP_200_OK,
    summary="Eliminar experiencia laboral",
    description="Elimina la experiencia laboral del usuario."
)
def delete_work_experience_endpoint(id: int, current_user: dict = Depends(check_user_role)):
    try:
        username = current_user["username"]
        message  = delete_work_experience(id, username)
        if message:
            return message
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se pudo encontrar la información de la experiencia laboral, el usuario '{username}' no existe o no tiene información asociada al id proporcionado."
            )
    except Exception as ex:
        logger.error(f'ro= Error inesperado al eliminar experiencia laboral: {str(ex)}')
        raise ex

# obtener la experiencia laboral por total en años
@router.get(
    "/work_experience/total_years/{username}",
    tags=['work_experience'],
    summary="Obtener la experiencia laboral total en años de un usuario",
    description="Este endpoint permite obtener la experiencia laboral total en años de un usuario"
)
def get_total_work_experience_endpoint(username: str):
    try:
        total_years = get_total_work_experience(username)
        return total_years
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al obtener la experiencia laboral: {str(ex)}')
        raise ex