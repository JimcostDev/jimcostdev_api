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