from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.work_experience_db import (
    get_work_experiences_by_user
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