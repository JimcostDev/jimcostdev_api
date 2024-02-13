from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.certification_db import (
    create_certification,
    get_certifications_by_user,
    update_certification,
    delete_certification
)
from database.models.certification_model import CertificationResponseModel, CertificationModel
import logging
from fastapi import status, HTTPException
import logging


logger = logging.getLogger(__name__)
router = APIRouter()

# crear certificación
@router.post(
    "/certification",
    tags=['certifications'],
    status_code=status.HTTP_201_CREATED,
    summary="Crear certificación",
    description="Crea nueva certificación con los datos proporcionados."
)
def create_certification_endpoint(certification_data: CertificationModel, current_user: dict = Depends(check_user_role)):
    try:
        created_certification = create_certification(
            certification_data, username=current_user["username"])
        if created_certification:
            return created_certification
    except Exception as ex:
        logger.error(f'ro= Error inesperado al crear certificación: {str(ex)}')
        raise ex

# obtener certificaciones por usuario
@router.get(
    "/certification/{username}",
    tags=['certifications'],
    response_model=List[CertificationResponseModel],
    summary="Obtener todas las certificaciones de un usuario",
    description="Este endpoint permite obtener todas las certificaciones de un usuario"
)
def get_certifications_endpoint(username: str):
    try:
        certifications = get_certifications_by_user(username)

        if certifications == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar certificaciones para el usuario, '{username}'")
        return certifications
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al obtener certificaciones: {str(ex)}')
        raise ex


# actualizar certificación
@router.put(
    "/certification/{username}",
    tags=['certifications'],
    summary="Actualizar certificación",
    description="Actualiza los datos de una certificación",
    status_code=status.HTTP_200_OK
)
def update_certification_endpoint(username: str, updated_info: CertificationModel, current_user: dict = Depends(check_user_role)):
    try:
        # Verificar que el usuario actual esté actualizando su propia información
        if current_user["username"] != username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para actualizar la información de otro usuario."
            )
        message = update_certification(username, updated_info)
        return message
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al actualizar certificación: {str(ex)}')
        raise ex


# eliminar certificación
@router.delete(
    "/certification/{username}",
    tags=['certifications'],
    summary="Eliminar certificación",
    description="Elimina la certificación del usuario",
    status_code=status.HTTP_200_OK
)
def delete_certification_endpoint(username: str, current_user: dict = Depends(check_user_role)):
    try:
        # Verificar que el usuario actual esté eliminando su propia información
        if current_user["username"] != username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar la información de otro usuario."
            )
        message = delete_certification(username)
        if message:
            return message
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se pudo encontrar la certificación, el usuario '{username}' no existe o no tiene certificaciones"
            )
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al eliminar certificación: {str(ex)}')
        raise ex
