from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.project_db import (
    create_project,
    add_skill,
    remove_skill,
    get_projects_by_user,
    update_project,
    delete_project
)
from database.models.project_model import ProjectModel, ProjectResponseModel
import logging
from fastapi import status, HTTPException
import logging


logger = logging.getLogger(__name__)
router = APIRouter()

# crear proyecto
@router.post(
    "/project",
    tags=['project'],
    status_code=status.HTTP_201_CREATED,
    summary="Crear proyecto",
    description="Crea un nuevo proyecto con los datos proporcionados."
)
def create_project_endpoint(project_data: ProjectModel, current_user: dict = Depends(check_user_role)):
    try:
        created_project = create_project(project_data, username=current_user["username"])
        if created_project:
            return created_project
    except Exception as ex:
        logger.error(f'ro= Error inesperado al crear project: {str(ex)}')
        raise ex
    
# agregar habilidades al stack del proyecto
@router.post(
    "/project/skill/{id}",
    tags=['project'],
    status_code=status.HTTP_200_OK,
    summary="Agregar habilidad al stack",
    description="Agrega una habilidad al stack del proyecto."
)
def add_skill_endpoint(skill: str, id: int, current_user: dict = Depends(check_user_role)):
    try:
        added_skill = add_skill(skill, id, username=current_user["username"])
        if added_skill:
            return added_skill
    except Exception as ex:
        logger.error(f'ro= Error inesperado al agregar habilidad al proyecto: {str(ex)}')
        raise ex
    
# remover habilidades al stack del proyecto
@router.delete(
    "/project/skill/{id}",
    tags=['project'],
    status_code=status.HTTP_200_OK,
    summary="Remover habilidad del stack",
    description="Remueve una habilidad del stack del proyecto."
)
def remove_skill_endpoint(skill: str, id: int, current_user: dict = Depends(check_user_role)):
    try:
        removed_skill = remove_skill(skill, id, username=current_user["username"])
        if removed_skill:
            return removed_skill
    except Exception as ex:
        logger.error(f'ro= Error inesperado al remover habilidad del project: {str(ex)}')
        raise ex
    

# obtener proyectos por usuario
@router.get(
    "/project/{username}",
    tags=['project'],
    response_model=List[ProjectResponseModel],
    summary="Obtener todas las proyectos de un usuario",
    description="Este endpoint permite obtener todos las proyectos de un usuario"
)
def get_projects_endpoint(username: str):
    try:
        projects = get_projects_by_user(username)

        if projects == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudieron encontrar proyectos para el usuario, '{username}'")
        return projects
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al obtener proyectos: {str(ex)}')
        raise ex

# actualizar project
@router.put(
    "/project/{id}",
    tags=['project'],
    status_code=status.HTTP_200_OK,
    summary="Actualizar proyecto",
    description="Actualiza el proyecto del usuario."
)
def update_project_endpoint(updated_info: ProjectModel, id: int, current_user: dict = Depends(check_user_role)):
    try:
        username = current_user["username"]
        message  = update_project(updated_info, id, username)
        return message
    except Exception as ex:
        logger.error(f'ro= Error inesperado al actualizar proyecto: {str(ex)}')
        raise ex

# eliminar project
@router.delete(
    "/project/{id}",
    tags=['project'],
    status_code=status.HTTP_200_OK,
    summary="Eliminar proyecto",
    description="Elimina el proyecto del usuario."
)
def delete_project_endpoint(id: int, current_user: dict = Depends(check_user_role)):
    try:
        username = current_user["username"]
        message  = delete_project(id, username)
        if message:
            return message
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se pudo encontrar la información de proyecto, el usuario '{username}' no existe o no tiene información asociada al id proporcionado."
            )
    except Exception as ex:
        logger.error(f'ro= Error inesperado al eliminar proyecto: {str(ex)}')
        raise ex