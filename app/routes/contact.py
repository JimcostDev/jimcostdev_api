from fastapi import (
    APIRouter, 
    HTTPException, 
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.contact_db import create_contact, get_contact_info_by_user
from database.models.contact_model import ContactModel, ContactResponseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# crear info de contacto
@router.post(
    "/contact",
    tags=['contact'],
    response_model=ContactModel,
    status_code=status.HTTP_201_CREATED,
    summary="Crear datos de contacto",
    description="Crea nueva información de contacto con los datos proporcionados."
)
def create_contact_endpoint(new_contact_data: ContactModel, current_user: dict = Depends(check_user_role)):
        try:
            created_contact = create_contact(new_contact_data, username=current_user["username"], email=current_user["email"])
            if created_contact:
                return created_contact
        except HTTPException as e:
            return e
        except Exception as ex:
            logger.error(f'rou= Error inesperado al crear el contacto: {str(ex)}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"rou= Error inesperado al crear el contacto: {str(ex)}"
            )

# consultar info de contacto por usuario
@router.get(
    "/contact/{username}", 
    tags=['contact'],
    response_model=ContactResponseModel,
    summary="Obtener datos de contacto del usuario",
    description="Este endpoint permite obtener los datos o la información de contacto del usuario"
)
def get_contact_endpoint(username: str):
    info_contact, http_status = get_contact_info_by_user(username)
    
    if http_status == status.HTTP_200_OK:
        return info_contact

    raise HTTPException(
        status_code=http_status,
        detail=f"Error al consultar información de contacto. Status Code: {http_status}"
    )