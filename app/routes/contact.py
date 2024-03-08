from fastapi import (
    APIRouter, 
    HTTPException, 
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.contact_db import (
    create_contact, 
    get_contact_info_by_user,
    update_contact,
    delete_contact 
)
from database.models.contact_model import ContactModel, ContactResponseModel
import logging
from fastapi import status, HTTPException
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


# actualizar info de contacto
@router.put(
    "/contact/{id}",
    tags=['contact'],
    status_code=status.HTTP_200_OK,
    summary="Actualizar datos de contacto",
    description="Actualiza la información de contacto con los datos proporcionados."
)
def update_contact_endpoint(updated_info: ContactModel, id: int, current_user: dict = Depends(check_user_role)):
        try:
            message = update_contact(updated_info, id, current_user["username"])
            return message
        
        except Exception as ex:
            logger.error(f'rou= Error inesperado al actualizar el contacto: {str(ex)}')
            raise ex

# eliminar info de contacto
@router.delete(
    "/contact/{id}",
    tags=['contact'],
    status_code=status.HTTP_200_OK,
    summary="Eliminar datos de contacto",
    description="Elimina la información de contacto del usuario."
)
def delete_contact_endpoint(id: int, current_user: dict = Depends(check_user_role)):
        try:
            username = current_user["username"]
            message = delete_contact(id, username)
            if message:
                return message
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se pudo encontrar la información de contacto, el usuario '{username}' no existe no tiene información asociada al id proporcionado."
                )
        except Exception as ex:
            logger.error(f'rou= Error inesperado al eliminar el contacto: {str(ex)}')
            raise ex