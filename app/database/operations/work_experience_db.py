from typing import List
from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.work_experience_model import WorkExperienceModel, WorkExperienceResponseModel
from utils.generate_id import obtener_ultimo_id
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# función para calcular la duración de una experiencia laboral
def calculate_duration(initial_date: str, end_date: str) -> str:
    if end_date is None:
        end_date_obj = datetime.now()
    else:
        end_date_obj = datetime.fromisoformat(end_date)
    
    initial_date_obj = datetime.fromisoformat(initial_date)
    duration = end_date_obj - initial_date_obj
    duration_years = duration.days // 365
    duration_months = (duration.days % 365) // 30
        
    
    if duration_years == 0:
        if duration_months <= 11:
            return f"{duration_months} meses"
        else:
            return f"{duration_months // 12} años"
    elif duration_months == 0:
        return f"{duration_years} años"
    elif duration_years == 1:
        if duration_months == 1:
            return "1 año y 1 mes"
        if duration_months == 12:
            return f"{duration_years + 1} años"
        else:
            return f"1 año y {duration_months} meses"
    else:
        if duration_months == 1:
            return f"{duration_years} años y 1 mes"
        if duration_months == 12:
            return f"{duration_years + 1} años"
        else:
            return f"{duration_years} años y {duration_months} meses"

# función para calcular la duración de una experiencia laboral en años
def calculate_duration_years(initial_date: str, end_date: str) -> float:
    if end_date is None:
        end_date_obj = datetime.now()
    else:
        end_date_obj = datetime.fromisoformat(end_date)
    
    initial_date_obj = datetime.fromisoformat(initial_date)
    duration = end_date_obj - initial_date_obj
    duration_years = duration.days / 365
    
    return duration_years


# obtener todas las experiencias laborales de un usuario
def get_work_experiences_by_user(username: str) -> List[WorkExperienceResponseModel]:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener la experiencia laboral del usuario
            work_experiences_cursor = db.work_experience_collection.find({"username": username}).sort("initial_date", -1)
            
            work_experiences_list = []
            for work_experience in work_experiences_cursor:
                # Calculamos la duración de la experiencia laboral
                duration = calculate_duration(work_experience['initial_date'], work_experience['end_date'])
                # Creamos el modelo de respuesta con la duración añadida
                work_experience_response = WorkExperienceResponseModel(
                    **work_experience,
                    id=work_experience.pop('_id'),
                    duration=duration
                )
                work_experiences_list.append(work_experience_response)
                
            return work_experiences_list
            
    except Exception as e:
        logger.exception(f"Ha ocurrido una excepción al obtener la experiencia laboral del usuario: {e}")
        raise e
    
# obtener la experiencia laboral por total en años
def get_total_work_experience(username: str) -> int:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener la experiencia laboral del usuario
            work_experiences_cursor = db.work_experience_collection.find({"username": username})
            
            total_work_experience = 0
            for work_experience in work_experiences_cursor:
                # Calculamos la duración de la experiencia laboral
                duration_years = calculate_duration_years(work_experience['initial_date'], work_experience['end_date'])
                print(total_work_experience)
                total_work_experience += duration_years

            return round(total_work_experience)
            
    except Exception as e:
        logger.exception(f"Ha ocurrido una excepción al obtener la experiencia laboral del usuario: {e}")
        raise e

# crear una nueva experiencia laboral
def create_work_experience(work_experience_data: WorkExperienceModel, username: str):
    try:
        # validar los datos del work_experience
        work_experience = work_experience_data.model_dump(exclude_unset=True)
                
        # ageregar el usuario que crea el work_experience
        work_experience["username"] = username

        # Convertir la fecha de inicio y fin a objetos str
        initial_date_str = work_experience['initial_date']
        work_experience['initial_date'] = str(initial_date_str)
        
        if work_experience['end_date'] is not None:
            end_date_str = work_experience['end_date']
            work_experience['end_date'] = str(end_date_str)
        else:
            work_experience['end_date'] = None
        
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
            ultimo_id = obtener_ultimo_id(db.work_experience_collection)
            
            # asignar el id al nuevo documento
            work_experience["_id"] = ultimo_id
            
            # insertar el documento en la colección
            result = db.work_experience_collection.insert_one(work_experience)
            
            # comprobar si el documento se insertó correctamente
            if result.inserted_id:
                message = {"message": "Experiencia laboral creada exitosamente"}
                return message 
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear el work_experience"
                )
    except Exception as e:
            logger.exception(f"Ha ocurrido una excepción al crear work_experience: {e}")
            raise e

# actualizar una experiencia laboral
def update_work_experience(updated_info: WorkExperienceModel, id: int, username: str):
    try:
        with get_database_instance() as db:
            existing = db.work_experience_collection.find_one({"username": username, "_id": id})
            if existing is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar información de la experiencia laboral, el usuario '{username}' no existe o no tiene información asociada al id proporcionado.")
            
            # convertir el modelo a un diccionario
            updated_values = updated_info.model_dump(exclude_unset=True)
            
            # Convertir la fecha de inicio y fin a objetos str
            initial_date_str = updated_values['initial_date']
            updated_values['initial_date'] = str(initial_date_str)
        
            if updated_values['end_date'] is not None:
                end_date_str = updated_values['end_date']
                updated_values['end_date'] = str(end_date_str)
            else:
                updated_values['end_date'] = None
            
            # actualizar y devolver el resultado
            result = db.work_experience_collection.update_one(
                {"username": username, "_id": id},
                {"$set": updated_values}
            )
            
            if result.matched_count  > 0 and result.modified_count > 0:
                message = {"message": "Experiencia laboral actualizada exitosamente"}
                return message
            else:
                message = {"message": "No se pudo actualizar la información de la experiencia laboral o no se encontraron cambios."}
                return message
    except Exception as e:
            logger.exception(f"Error al actualizar la información de la experiencia laboral: {e}")
            raise e

# eliminar una experiencia laboral
def delete_work_experience(id: int, username: str):
    try:
        with get_database_instance() as db:
            result = db.work_experience_collection.delete_one({"username": username, "_id": id})
            
            if result.deleted_count > 0:
                message = {"message": "Experiencia laboral eliminada exitosamente"}
                return message
            else:
                return None
    except Exception as e:
        logger.exception(f"Error al eliminar experiencia laboral: {e}")
        raise e
