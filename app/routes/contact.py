from fastapi import APIRouter, HTTPException, status
from database.operations.contact_db import create_contact, get_contact_info_by_user
from database.models.contact_model import ContactModel, ContactResponseModel

router = APIRouter()

# CREAR INFO DE CONTACTO
@router.post(
    "/contact",
    response_model=ContactModel,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo contacto",
    description="Crea un nuevo contacto con la información proporcionada."
)
def create_contact_endpoint(new_contact_data: ContactModel):
    """
    Crea un nuevo contacto.

    Args:
        new_contact_data (ContactModel): Datos del nuevo contacto.

    Returns:
        dict: Datos del contacto creado.
    """
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

# CONSULTAR INFO DE CONTACTO
@router.get(
    "/contact/{username}", 
    response_model=ContactResponseModel,
    summary="Consultar info de contacto por usuario",
    description="Este endpoint permite obtener la información detallada de contacto"
)
def get_contact_endpoint(user_name: str):
    info_contact, http_status = get_contact_info_by_user(user_name)
    
    if http_status == status.HTTP_200_OK:
        return info_contact

    raise HTTPException(
        status_code=http_status,
        detail=f"Error al consultar información de contacto. Status Code: {http_status}"
    )