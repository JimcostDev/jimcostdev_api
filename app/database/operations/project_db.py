from typing import List
from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.project_model import ProjectModel, ProjectResponseModel
from utils.generate_id import obtener_ultimo_id
import logging

logger = logging.getLogger(__name__)

# crear proyecto
def create_project(project_data: ProjectModel, username: str):
    try:
        # validar los datos del project
        project = project_data.model_dump(exclude_unset=True)
                
        # ageregar el usuario que crea el project
        project["username"] = username

        # Convertir la URL a una cadena (si es necesario)
        url_str = project['image']
        project['image'] = str(url_str)
        
        link_str = project['link']
        project['link'] = str(link_str)
        
    except ValidationError as e:
        # Manejar errores de validación Pydantic aquí
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error de validación: {e.errors()}"
        )
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener el último id de la colección de proyectos
            ultimo_id = obtener_ultimo_id(db.projects_collection)
            
            # asignar el id al nuevo documento
            project["_id"] = ultimo_id
            
            # insertar el documento en la colección
            result = db.projects_collection.insert_one(project)
            
            # comprobar si el documento se insertó correctamente
            if result.inserted_id:
                message = {"message": "Proyecto creado exitosamente"}
                return message 
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear el project"
                )
    except Exception as e:
            logger.exception(f"Ha ocurrido una excepción al crear project: {e}")
            raise e


# agregar skills al stack del proyecto
def add_skill(skill: str, id: int, username: str):
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Actualizar el documento en la colección
            result = db.projects_collection.update_one(
                {"username": username, "_id": id},
                {"$push": {"stack": skill}}
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

# remover skills al stack del proyecto
def remove_skill(skill: str, id: int, username: str):
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # comprobar si la habilidad existe en el project
            exists = db.projects_collection.find_one({"username": username, "stack": skill, "_id": id})
            
            if not exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La habilidad no existe en el stack del proyecto"
                )
            
            # Actualizar el documento en la colección
            result = db.projects_collection.update_one(
                {"username": username, "_id": id},
                {"$pull": {"stack": skill}}
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


# obtener proyectos por usuario
def get_projects_by_user(username: str) -> List[ProjectResponseModel]:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            # Obtener las proyectos del usuario
            projects_cursor = db.projects_collection.find({"username": username}).sort("title", -1)
            
            if projects_cursor:
                projects_list = [
                    ProjectResponseModel(**project, id=project.pop('_id'))
                    for project in projects_cursor
                ]
                return projects_list
            else:
                return []
    except Exception as e:
        logger.exception(f"Ha ocurrido una excepción al obtener las proyectos del usuario: {e}")
        raise e

# actualizar project
def update_project(updated_info: ProjectModel, id: int, username: str):
    try:
        with get_database_instance() as db:
            existing = db.projects_collection.find_one({"username": username, "_id": id})
            if existing is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar información del proyecto, el usuario '{username}' no existe o no tiene información asociada al id proporcionado.")
            
            # convertir el modelo a un diccionario
            updated_values = updated_info.model_dump(exclude_unset=True)
            
            # Convertir la URL a una cadena (si es necesario)
            url_str = updated_values['image']
            updated_values['image'] = str(url_str)
            
            link_str = updated_values['link']
            updated_values['link'] = str(link_str)
            
            # actualizar y devolver el resultado
            result = db.projects_collection.update_one(
                {"username": username, "_id": id},
                {"$set": updated_values}
            )
            
            if result.matched_count  > 0 and result.modified_count > 0:
                message = {"message": "Proyecto actualizado exitosamente"}
                return message
            else:
                message = {"message": "No se pudo actualizar la información del proyecto o no se encontraron cambios."}
                return message
    except Exception as e:
            logger.exception(f"Error al actualizar la información de proyecto: {e}")
            raise e

# eliminar project
def delete_project(id: int, username: str):
    try:
        with get_database_instance() as db:
            result = db.projects_collection.delete_one({"username": username, "_id": id})
            
            if result.deleted_count > 0:
                message = {"message": "Proyecto eliminado exitosamente"}
                return message
            else:
                return None
    except Exception as e:
        logger.exception(f"Error al eliminar proyecto: {e}")
        raise e