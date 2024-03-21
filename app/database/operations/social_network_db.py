from typing import List
from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.social_network_model import SocialNetworkModel, SocialNetworkResponseModel
from utils.generate_id import obtener_ultimo_id
import logging

logger = logging.getLogger(__name__)

# crear red social
def create_social_network(social_network_data: SocialNetworkModel, username: str):
    try:
        # validar los datos de la red social
        social_network = social_network_data.model_dump(exclude_unset=True)
                
        # ageregar el usuario que crea la red social
        social_network["username"] = username

        # Convertir la URL a una cadena (si es necesario)
        url_str = social_network['url']
        social_network['url'] = str(url_str)
        
    except ValidationError as e:
        # Manejar errores de validación Pydantic aquí
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error de validación: {e.errors()}"
        )
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener el último id de la colección de redes sociales
            ultimo_id = obtener_ultimo_id(db.social_networks_collection)
            
            # asignar el id al nuevo documento
            social_network["_id"] = ultimo_id
            
            # insertar el documento en la colección
            result = db.social_networks_collection.insert_one(social_network)
            
            # comprobar si el documento se insertó correctamente
            if result.inserted_id:
                message = {"message": "Red social creada exitosamente"}
                return message 
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear la red social"
                )
    except Exception as e:
            logger.exception(f"Ha ocurrido una excepción al crear red social: {e}")
            raise e

# obtener redes sociales por usuario
def get_social_networks_by_user(username: str) -> List[SocialNetworkResponseModel]:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener las redes sociales del usuario
            social_networks_cursor = db.social_networks_collection.find({"username": username})
            
            if social_networks_cursor:
                social_networks_list = [
                    SocialNetworkResponseModel(**social_network, id=social_network.pop('_id'))
                    for social_network in social_networks_cursor
                ]
                return social_networks_list
            else:
                return []
    except Exception as e:
        logger.exception(f"Ha ocurrido una excepción al obtener las redes sociales del usuario: {e}")
        raise e

# actualizar red social
def update_social_network(updated_info: SocialNetworkModel, id: int, username: str):
    try:
        with get_database_instance() as db:
            existing = db.social_networks_collection.find_one({"username": username, "_id": id})
            if existing is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar red social, el usuario '{username}' no existe o no tiene información asociada al id proporcionado.")
            
            # convertir el modelo a un diccionario
            updated_values = updated_info.model_dump(exclude_unset=True)
            
            # Convertir la URL a una cadena (si es necesario)
            url_str = updated_values['url']
            updated_values['url'] = str(url_str)
            
            # actualizar y devolver el resultado
            result = db.social_networks_collection.update_one(
                {"username": username, "_id": id},
                {"$set": updated_values}
            )
            
            if result.matched_count  > 0 and result.modified_count > 0:
                message = {"message": "Red social actualizada exitosamente"}
                return message
            else:
                message = {"message": "No se pudo actualizar la red social o no se encontraron cambios."}
                return message
    except Exception as e:
            logger.exception(f"Error al actualizar la red social: {e}")
            raise e

# eliminar red social
def delete_social_network(id: int, username: str):
    try:
        with get_database_instance() as db:
            result = db.social_networks_collection.delete_one({"username": username, "_id": id})
            
            if result.deleted_count > 0:
                message = {"message": "Red social eliminada exitosamente"}
                return message
            else:
                return None
    except Exception as e:
        logger.exception(f"Error al eliminar red social: {e}")
        raise e