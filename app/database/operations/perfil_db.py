from typing import List
from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.perfil_model import PerfilModel, PerfilResponseModel
from utils.generate_id import obtener_ultimo_id
import logging

logger = logging.getLogger(__name__)

# crear perfil
def create_perfil(perfil_data: PerfilModel, username: str):
    try:
        # validar los datos del perfil
        perfil = perfil_data.model_dump(exclude_unset=True)
                
        # ageregar el usuario que crea el perfil
        perfil["username"] = username

        # Convertir la URL a una cadena (si es necesario)
        url_str = perfil['avatar']
        perfil['avatar'] = str(url_str)
        
    except ValidationError as e:
        # Manejar errores de validación Pydantic aquí
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error de validación: {e.errors()}"
        )
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener el último id de la colección de certificaciones
            ultimo_id = obtener_ultimo_id(db.perfil_collection)
            
            # asignar el id al nuevo documento
            perfil["_id"] = ultimo_id
            
            # insertar el documento en la colección
            result = db.perfil_collection.insert_one(perfil)
            
            # comprobar si el documento se insertó correctamente
            if result.inserted_id:
                message = {"message": "Perfil creado exitosamente"}
                return message 
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear el perfil"
                )
    except Exception as e:
            logger.exception(f"Ha ocurrido una excepción al crear perfil: {e}")
            raise e
    

# agregar habilidades al perfil
def add_skill(skill: str, username: str):
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Actualizar el documento en la colección
            result = db.perfil_collection.update_one(
                {"username": username},
                {"$push": {"skills": skill}}
            )
            
            # comprobar si el documento se actualizó correctamente
            if result.modified_count:
                message = {"message": "Habilidad agregada exitosamente"}
                return message
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al agregar la habilidad"
                )
    except Exception as e:
            logger.exception(f"Ha ocurrido una excepción al agregar habilidad: {e}")
            raise e

# remover habilidades del perfil
def remove_skill(skill: str, username: str):
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # comprobar si la habilidad existe en el perfil
            exists = db.perfil_collection.find_one({"username": username, "skills": skill})
            
            if not exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La habilidad no existe en el perfil"
                )
            
            # Actualizar el documento en la colección
            result = db.perfil_collection.update_one(
                {"username": username},
                {"$pull": {"skills": skill}}
            )
            
            # comprobar si el documento se actualizó correctamente
            if result.modified_count:
                message = {"message": "Habilidad removida exitosamente"}
                return message
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al remover la habilidad"
                )
    except Exception as e:
            logger.exception(f"Ha ocurrido una excepción al remover habilidad: {e}")
            raise e

# obtener perfil
def get_perfil(username: str) -> PerfilResponseModel:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            perfil = db.perfil_collection.find_one({"username": username})

            if perfil:
                perfil['id'] = perfil.pop('_id')
                return perfil
            else:
                None
    except Exception as e:
        raise e


# actualizar perfil
def update_perfil(updated_info: PerfilModel, id: int, username: str):
    try:
        with get_database_instance() as db:
            existing = db.perfil_collection.find_one({"username": username, "_id": id})
            if existing is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar información de perfil, el usuario '{username}' no existe o no tiene información asociada al id proporcionado.")
            
            # convertir el modelo a un diccionario
            updated_values = updated_info.model_dump(exclude_unset=True)
            
            # Convertir la URL a una cadena (si es necesario)
            url_str = updated_values['avatar']
            updated_values['avatar'] = str(url_str)
            
            # actualizar y devolver el resultado
            result = db.perfil_collection.update_one(
                {"username": username, "_id": id},
                {"$set": updated_values}
            )
            
            if result.matched_count  > 0 and result.modified_count > 0:
                message = {"message": "Perfil actualizado exitosamente"}
                return message
            else:
                message = {"message": "No se pudo actualizar la información de perfil o no se encontraron cambios."}
                return message
    except Exception as e:
            logger.exception(f"Error al actualizar la información de perfil: {e}")
            raise e

# eliminar perfil
def delete_perfil(id: int, username: str):
    try:
        with get_database_instance() as db:
            result = db.perfil_collection.delete_one({"username": username, "_id": id})
            
            if result.deleted_count > 0:
                message = {"message": "Perfil eliminado exitosamente"}
                return message
            else:
                return None
    except Exception as e:
        logger.exception(f"Error al eliminar perfil: {e}")
        raise e