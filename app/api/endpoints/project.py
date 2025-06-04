from fastapi import APIRouter, Body, Depends, status
from models.project_model import (
    ProjectCreate,
    ProjectResponse
)
from services.project_service import ProjectService
from utils.auth_manager import check_admin_role

router = APIRouter(prefix="/projects")
service = ProjectService()

# -- GET públicos con prefijo /p/ --
@router.get(
    "/p/{username}",
    response_model=list[ProjectResponse],
    summary="Obtener proyectos de usuario",
    description="Obtiene el proyectos de un usuario por su nombre"
)
async def list_projects(username: str):
    return await service.list_projects(username)

@router.get(
    "/p/{username}/{id}",
    response_model=ProjectResponse,
    summary="Obtener proyecto por ID y usuario",
    description="Obtiene una proyecto específica de un usuario por su ID"
)
async def get_project(username: str, id: str):
    return await service.get_project(id, username)

# -- Operaciones privadas (POST, PUT, DELETE) --
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear proyectos",
    description="Crear proyectos para el usuario autenticado",
)
async def create_project(
    payload: ProjectCreate,
    current_user=Depends(check_admin_role)
):
    return await service.create_project(payload, current_user.username)
    
    

@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ProjectResponse,
    summary="Actualizar proyectos",
    description="Actualiza proyectos existente del usuario autenticado por su ID",
)
async def update_project(
    id: str,
    payload: ProjectCreate,
    current_user=Depends(check_admin_role)
):
    return await service.update_project(id, payload, current_user.username)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar proyectos",
    description="Elimina proyectos del usuario autenticado por su ID",
)
async def delete_project(
    id: str,
    current_user=Depends(check_admin_role)
):
    await service.delete_project(id, current_user.username)
    
# -- Nuevos endpoints para stack (skills) --
@router.post(
    "/{id}/skill",
    status_code=status.HTTP_200_OK,
    summary="Agregar skill al proyecto",
    description="Agrega una skill al stack de un proyecto del usuario autenticado"
)
async def add_skill_to_project(
    id: str,
    skill: str = Body(..., embed=True, description="Nombre de la skill a agregar"),
    current_user=Depends(check_admin_role)
):
    return await service.add_skill(skill, id, current_user.username)


@router.delete(
    "/{id}/skill/{skill}",
    status_code=status.HTTP_200_OK,
    summary="Remover skill del proyecto",
    description="Remueve una skill del stack de un proyecto del usuario autenticado"
)
async def remove_skill_from_project(
    id: str,
    skill: str,
    current_user=Depends(check_admin_role)
):
    return await service.remove_skill(skill, id, current_user.username)


  
    
    