from typing import List
from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.work_experience_model import WorkExperienceModel, WorkExperienceResponseModel
from utils.generate_id import obtener_ultimo_id
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

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
        else:
            return f"1 año y {duration_months} meses"
    else:
        if duration_months == 1:
            return f"{duration_years} años y 1 mes"
        else:
            return f"{duration_years} años y {duration_months} meses"

# obtener todas las experiencias laborales de un usuario
def get_work_experiences_by_user(username: str) -> List[WorkExperienceResponseModel]:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener la experiencia laboral del usuario
            work_experiences_cursor = db.work_experience_collection.find({"username": username})
            
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
