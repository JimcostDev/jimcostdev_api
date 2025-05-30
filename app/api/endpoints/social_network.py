from fastapi import APIRouter, Depends, status
from models.social_network_model import (
    SocialNetworkCreate,
    SocialNetworkResponse
)
from services.social_network_service import SocialNetworkService
from utils.auth_manager import check_admin_role
from exceptions import (
    NotFoundException,
    ConflictException,
    DatabaseException
)

router = APIRouter(prefix="/social_networks")
service = SocialNetworkService()

# -- GET públicos con prefijo /p/ --
@router.get(
    "/p/{username}",
    response_model=list[SocialNetworkResponse],
    summary="Listar redes sociales de usuario",
    description="Obtiene todas las redes sociales de un usuario por su nombre"
)
async def list_social_networks(username: str):
    return await service.list_social_networks(username)

@router.get(
    "/p/{username}/{id}",
    response_model=SocialNetworkResponse,
    summary="Obtener red social por ID",
    description="Obtiene una red social específica por su ID y usuario"
)
async def get_social_network(username: str, id: str):
    try:
        return await service.get_social_network(id, username)
    except NotFoundException as e:
        raise e

# -- Operaciones privadas (POST, PUT, DELETE) --
@router.post(
    "/",
    response_model=SocialNetworkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva red social",
    description="Crea una nueva red social (requiere autenticación)"
)
async def create_social_network(
    payload: SocialNetworkCreate,
    current_user=Depends(check_admin_role)
):
    try:
        return await service.create_social_network(payload, current_user.username)
    except ConflictException as e:
        raise e
    except Exception as e:
        raise DatabaseException(str(e))

@router.put(
    "/{id}",
    response_model=SocialNetworkResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar red social",
    description="Actualiza una red social existente (requiere autenticación)"
)
async def update_social_network(
    id: str,
    payload: SocialNetworkCreate,
    current_user=Depends(check_admin_role)
):
    try:
        return await service.update_social_network(id, payload, current_user.username)
    except (NotFoundException, ConflictException) as e:
        raise e
    except Exception as e:
        raise DatabaseException(str(e))

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar red social",
    description="Elimina una red social existente (requiere autenticación)"
)
async def delete_social_network(
    id: str,
    current_user=Depends(check_admin_role)
):
    try:
        await service.delete_social_network(id, current_user.username)
    except NotFoundException as e:
        raise e