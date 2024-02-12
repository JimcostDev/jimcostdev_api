from typing import List
from fastapi import (
    APIRouter, 
    HTTPException, 
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.certification_db import (
    create_certification,
    get_certifications_by_user
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
        created_certification = create_certification(certification_data, username=current_user["username"])
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
        
        if  certifications == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar certificaciones para el usuario, '{username}'")
        return certifications
    except Exception as ex:
        logger.error(f'rou= Error inesperado al obtener certificaciones: {str(ex)}')
        raise ex