from typing import List
from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.certification_model import CertificationModel, CertificationResponseModel
from utils.generate_id import obtener_ultimo_id
import logging

logger = logging.getLogger(__name__)

# crear certificación
def create_certification(certification_data: CertificationModel, username: str):
    try:
        # validar los datos de la certificación
        certification = certification_data.model_dump(exclude_unset=True)
                
        # ageregar el usuario que crea la certificación
        certification["username"] = username

        # Convertir la URL a una cadena (si es necesario)
        url_str = certification['link']
        certification['link'] = str(url_str)
        
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
            ultimo_id = obtener_ultimo_id(db.certifications_collection)
            
            # asignar el id al nuevo documento
            certification["_id"] = ultimo_id
            
            # insertar el documento en la colección
            result = db.certifications_collection.insert_one(certification)
            
            # comprobar si el documento se insertó correctamente
            if result.inserted_id:
                message = {"message": "Certificación creada exitosamente"}
                return message 
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear la certificación"
                )
    except Exception as e:
            logger.exception(f"Ha ocurrido una excepción al crear cretificación: {e}")
            raise e


# obtener certificaciones por usuario
def get_certifications_by_user(username: str) -> List[CertificationResponseModel]:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener las certificaciones del usuario
            certifications_cursor = db.certifications_collection.find({"username": username})
            
            if certifications_cursor:
                certifications_list = [
                    CertificationResponseModel(**certification, id=certification.pop('_id'))
                    for certification in certifications_cursor
                ]
                return certifications_list
            else:
                return []
    except Exception as e:
        logger.exception(f"Ha ocurrido una excepción al obtener las certificaciones del usuario: {e}")
        raise e
    