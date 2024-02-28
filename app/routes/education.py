from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.education_db import (
    get_education_by_user,
    create_education
)
from database.models.education_model import EducationResponseModel, EducationModel
import logging
from fastapi import status, HTTPException
import logging


logger = logging.getLogger(__name__)
router = APIRouter()


# obtener educación por usuario
@router.get(
    "/education/{username}",
    tags=['education'],
    response_model=List[EducationResponseModel],
    summary="Obtener la educación de un usuario",
    description="Este endpoint permite obtener la educación de un usuario"
)
def get_education_endpoint(username: str):
    try:
        educations = get_education_by_user(username)

        if educations == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar educación para el usuario, '{username}'")
        return educations
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al obtener educación: {str(ex)}')
        raise ex
    
# crear educación
@router.post(
    "/education",
    tags=['education'],
    status_code=status.HTTP_201_CREATED,
    summary="Crear educación",
    description="Crea nueva educación con los datos proporcionados."
)
def create_education_endpoint(education_data: EducationModel, current_user: dict = Depends(check_user_role)):
    try:
        created_education = create_education(
            education_data, username=current_user["username"])
        if created_education:
            return created_education
    except Exception as ex:
        logger.error(f'ro= Error inesperado al crear educación: {str(ex)}')
        raise ex