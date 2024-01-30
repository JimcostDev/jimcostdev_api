from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.contact_model import ContactModel
from utils.generate_id import obtener_ultimo_id
import logging

logger = logging.getLogger(__name__)

# crear contacto
def create_contact(new_contact_data: ContactModel, username: str, email: str):
    try:
        # Validar los datos del nuevo contacto utilizando el modelo
        contact_data = new_contact_data.dict(exclude_unset=True)
       
        web_url_str = contact_data['web']['url']
        
        # Convertir la URL a una cadena (si es necesario)
        contact_data['web']['url'] = str(web_url_str)
        
        # Agregar el username y email al documento del contacto
        contact_data['username'] = username
        contact_data['email'] = email   
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
                return ContactModel(**contact_data).dict()
            else:
                # Devolver el código de estado 500 si la inserción falla
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al insertar el contacto en la base de datos")
    except Exception as ex:
        logger.error(f'op= Error inesperado al crear el contacto: {str(ex)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"op= Error inesperado al crear el contacto: {str(ex)}"
        )

# obtener info de contacto
def get_contact_info_by_user(username: str) -> dict:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            info_contact = db.contact_collection.find_one({"username": username})

            if info_contact:
                info_contact['id'] = info_contact.pop('_id')
                return info_contact, status.HTTP_200_OK
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar la información de contacto, el usuario '{username}' no existe.")
    except Exception as e:
        raise e


# actualizar contacto
def update_contact(username: str, updated_info: ContactModel):
    with get_database_instance() as db:
        try:
            existing_info = db.contact_collection.find_one({"username": username})
            if existing_info is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar la información de contacto, el usuario '{username}' no existe.")

            # Convertir ContactModel a un diccionario
            updated_values = updated_info.model_dump(exclude_unset=True)

            # Convertir la URL a una cadena (si es necesario)
            web_url_str = updated_values['web']['url']
            updated_values['web']['url'] = str(web_url_str)

            # Actualizar y obtener el resultado
            result = db.contact_collection.update_one(
                {"username": username},
                {"$set": updated_values}
            )

            if result.matched_count > 0 and result.modified_count > 0:
                message = {"message": "Usuario actualizado exitosamente"}
                return message
            else:
                message = {"message": "No se realizó ninguna actualización"}
                return message
        except Exception as e:
            logger.exception(f"Error al actualizar el usuario: {e}")
            raise e
