from typing import List
from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.education_model import EducationModel, EducationResponseModel
from utils.generate_id import obtener_ultimo_id
import logging

logger = logging.getLogger(__name__)

# obtener educación por usuario
def get_education_by_user(username: str) -> List[EducationResponseModel]:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener las educación del usuario ordenadas por año de graduación
            educations_cursor = db.education_collection.find({"username": username}).sort("year", -1)
            
            if educations_cursor:
                educations_list = [
                    EducationResponseModel(**education, id=education.pop('_id'))
                    for education in educations_cursor
                ]
                return educations_list
            else:
                return []
    except Exception as e:
        logger.exception(f"Ha ocurrido una excepción al obtener la educación del usuario: {e}")
        raise e
    
# crear educación
def create_education(education_data: EducationModel, username: str):
    try:
        # validar los datos de la educación
        education = education_data.model_dump(exclude_unset=True)
                
        # ageregar el usuario que crea la educación
        education["username"] = username
        
    except ValidationError as e:
        # Manejar errores de validación Pydantic aquí
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error de validación: {e.errors()}"
        )
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener el último id de la colección de educación
            ultimo_id = obtener_ultimo_id(db.education_collection)
            
            # asignar el id al nuevo documento
            education["_id"] = ultimo_id
            
            # insertar el documento en la colección
            result = db.education_collection.insert_one(education)
            
            # comprobar si el documento se insertó correctamente
            if result.inserted_id:
                message = {"message": "Educación creada exitosamente"}
                return message 
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear la educación"
                )
    except Exception as e:
            logger.exception(f"Ha ocurrido una excepción al crear educación: {e}")
            raise e

# actualizar educación
def update_education(updated_info: EducationModel, id_education: int, username: str):
    try:
        with get_database_instance() as db:
            existing = db.education_collection.find_one({"username": username})
            if existing is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar educación, el usuario '{username}' no existe o no tiene estudios creados")
            
            # convertir el modelo a un diccionario
            updated_values = updated_info.model_dump(exclude_unset=True)
            # ageregar el usuario que crea la educación
            updated_values["username"] = username
            
            # actualizar y devolver el resultado
            result = db.education_collection.update_one(
                {"username": 'username', "_id": id_education},
                {"$set": updated_values}
            )
            print(f'resultado:{result.matched_count}')
            if result.matched_count  > 0 and result.modified_count > 0:
                message = {"message": "Educación actualizada exitosamente"}
                return message
            else:
                message = {"message": "No se pudo actualizar la educación o no se encontraron cambios."}
                return message
    except Exception as e:
            logger.exception(f"Error al actualizar la información de educación: {e}")
            raise e

# eliminar educación
def delete_education(id: int , username: str, ):
    try:
        with get_database_instance() as db:
            result = db.education_collection.delete_one({"username": username, "_id": id})
            
            if result.deleted_count > 0:
                message = {"message": "Educación eliminada exitosamente"}
                return message
            else:
                return None
    except Exception as e:
        logger.exception(f"Error al eliminar educación: {e}")
        raise e