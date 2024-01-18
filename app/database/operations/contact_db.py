from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.contact_model import ContactModel
from utils.generate_id import obtener_ultimo_id

# crear contacto
def create_contact(new_contact_data: ContactModel):
    """
    Crea un nuevo contacto en la base de datos.

    Args:
        new_contact_data (ContactModel): Datos del nuevo contacto.

    Returns:
        tuple: Una tupla que contiene el contacto y el código de estado HTTP.
    """
    try:
        # Validar los datos del nuevo contacto utilizando el modelo
        contact_data = new_contact_data.dict()
        web_url_str = contact_data['web']['url']
        
        # Convertir la URL a una cadena (si es necesario)
        contact_data['web']['url'] = str(web_url_str)
            
    except ValidationError as e:
        # Manejar errores de validación Pydantic aquí
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error de validación: {e.errors()}"
        )

    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener el último id de la colección 'contact'
            ultimo_id = obtener_ultimo_id(db.contact_collection)

            # Asignar el nuevo id al documento del contacto
            contact_data["_id"] = ultimo_id

            # Insertar el nuevo contacto en la colección 'contact'
            result = db.contact_collection.insert_one(contact_data)
        
            # Comprobar si la inserción fue exitosa
            if result.inserted_id:
                # Devolver una instancia del modelo ContactModel y el código de estado 201
                return ContactModel(**contact_data).dict(), status.HTTP_201_CREATED
            else:
                # Devolver el código de estado 500 si la inserción falla
                return None, status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as ex:
        # Devolver el código de estado 500 y los detalles de la excepción
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al crear el contacto: {str(ex)}"
        )

# obtenert info de contacti por id
def get_contact_info_by_user(user_name: int) -> dict:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            info_contact = db.contact_collection.find_one({"username": user_name})

            if info_contact:
                info_contact['id'] = info_contact.pop('_id')
                return info_contact, status.HTTP_200_OK
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar la información de contacto, el usuario '{user_name}' no existe.")
    except Exception as e:
        # No es necesario levantar una HTTPException aquí para errores internos
        # FastAPI responderá automáticamente con un código de estado 500
        raise e
