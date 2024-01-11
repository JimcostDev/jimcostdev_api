from fastapi import APIRouter, HTTPException, status
from database.operations.contact_db import create_contact
from database.models.contact_model import ContactModel

router = APIRouter()


# CREAR INFO DE CONTACTO
@router.post(
    "/contact",
    response_model=dict,
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
        created_contact = create_contact(new_contact_data)
        return created_contact
    except HTTPException as e:
        # Devolver la excepción HTTP con los detalles apropiados
        raise e
    except Exception as ex:
        # Manejar otras excepciones inesperadas
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al crear el contacto: {str(ex)}"
        )
