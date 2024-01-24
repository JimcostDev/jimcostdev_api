from fastapi import (
    APIRouter, 
    HTTPException, 
    status, Depends
)
from database.conn_db import get_database_instance
from utils.auth_manager import check_user_role
from database.operations.contact_db import create_contact, get_contact_info_by_user
from database.models.contact_model import ContactModel, ContactResponseModel

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
def create_contact_endpoint(new_contact_data: ContactModel = Depends(check_user_role)):
        try:
            created_contact, http_status = create_contact(new_contact_data)

            if http_status == status.HTTP_201_CREATED:
                return created_contact

            raise HTTPException(
                status_code=http_status,
                detail=f"Error al crear el contacto. Status Code: {http_status}"
            )
        except HTTPException as e:
            return e
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error inesperado al crear el contacto: {str(ex)}"
            )

# consultar info de contacto por usuario
@router.get(
    "/contact/{username}", 
    tags=['contact'],
    response_model=ContactResponseModel,
    summary="Obtener datos de contacto del usuario",
    description="Este endpoint permite obtener los datos o la información de contacto del usuario"
)
def get_contact_endpoint(user_name: str):
    info_contact, http_status = get_contact_info_by_user(user_name)
    
    if http_status == status.HTTP_200_OK:
        return info_contact

    raise HTTPException(
        status_code=http_status,
        detail=f"Error al consultar información de contacto. Status Code: {http_status}"
    )