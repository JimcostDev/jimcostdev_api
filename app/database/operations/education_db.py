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