from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    status, Depends
)
from utils.auth_manager import check_user_role
from database.operations.social_network_db import (
    create_social_network,
    get_social_networks_by_user,
    update_social_network,
    delete_social_network
)
from database.models.social_network_model import SocialNetworkModel, SocialNetworkResponseModel
import logging
from fastapi import status, HTTPException
import logging


logger = logging.getLogger(__name__)
router = APIRouter()


# crear red social
@router.post(
    "/social_network",
    tags=['social_network'],
    status_code=status.HTTP_201_CREATED,
    summary="Crear red social",
    description="Crea nueva red social con los datos proporcionados."
)
def create_social_network_endpoint(social_network_data: SocialNetworkModel, current_user: dict = Depends(check_user_role)):
    try:
        created_social_network = create_social_network(social_network_data, username=current_user["username"])
        if created_social_network:
            return created_social_network
    except Exception as ex:
        logger.error(f'ro= Error inesperado al crear red social: {str(ex)}')
        raise ex

# obtener redes sociales por usuario
@router.get(
    "/social_network/{username}",
    tags=['social_network'],
    response_model=List[SocialNetworkResponseModel],
    summary="Obtener todas las redes sociales de un usuario",
    description="Este endpoint permite obtener todas las redes sociales de un usuario"
)
def get_social_networks_endpoint(username: str):
    try:
        social_networks = get_social_networks_by_user(username)

        if social_networks == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudieron encontrar redes sociales para el usuario, '{username}'")
        return social_networks
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al obtener redes sociales: {str(ex)}')
        raise ex

# actualizar red social
@router.put(
    "/social_network/{id}",
    tags=['social_network'],
    summary="Actualizar red social",
    description="Actualiza los datos de una red social",
    status_code=status.HTTP_200_OK
)
def update_social_network_endpoint(updated_info: SocialNetworkModel, id: int, current_user: dict = Depends(check_user_role)):
    try:
        username = current_user["username"]
        message = update_social_network(updated_info, id, username)
        return message
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al actualizar red social: {str(ex)}')
        raise ex


# eliminar red social
@router.delete(
    "/social_network/{id}",
    tags=['social_network'],
    summary="Eliminar red social",
    description="Elimina la red social del usuario",
    status_code=status.HTTP_200_OK
)
def delete_social_network_endpoint(id: int, current_user: dict = Depends(check_user_role)):
    try:
        username = current_user["username"]
        message = delete_social_network(id, username)
        if message:
            return message
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se pudo encontrar la red social, el usuario '{username}' no existe o no tiene información asociada al id proporcionado."
            )
    except Exception as ex:
        logger.error(
            f'rou= Error inesperado al eliminar red social: {str(ex)}')
        raise ex