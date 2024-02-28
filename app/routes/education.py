from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.education_db import (
    get_education_by_user,
    create_education,
    update_education,
    delete_education
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
        education = get_education_by_user(username)

        if education == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar educación para el usuario, '{username}'")
        return education
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
    

# actualizar educación
@router.put(
    "/education/{id_education}",
    tags=['education'],
    summary="Actualizar educación",
    description="Actualiza los datos de una educación",
    status_code=status.HTTP_200_OK
)
def update_education_endpoint(updated_info: EducationModel, id_education: int, current_user: dict = Depends(check_user_role)):
    try:
        # Verificar que el usuario actual esté actualizando su propia información
        if current_user["username"] != current_user["username"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para actualizar la información de otro usuario."
            )
        message = update_education(updated_info, id_education, username=current_user["username"])
        return message
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al actualizar educación: {str(ex)}')
        raise ex


# eliminar educación
@router.delete(
    "/education/{id}",
    tags=['education'],
    summary="Eliminar educación",
    description="Elimina la educación del usuario",
    status_code=status.HTTP_200_OK
)
def delete_education_endpoint(id: int, current_user: dict = Depends(check_user_role)):
    try:
        # Verificar que el usuario actual esté eliminando su propia información
        if current_user["username"] != current_user["username"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar la información de otro usuario."
            )
        username = current_user["username"]
        message = delete_education(id, username)
        if message:
            return message
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se pudo encontrar la educación, el usuario '{username}' no existe o no tiene información de estudios"
            )
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al eliminar educación: {str(ex)}')
        raise ex