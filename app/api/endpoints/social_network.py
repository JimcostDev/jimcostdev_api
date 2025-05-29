from fastapi import APIRouter, Depends, status
from typing import List
from models.social_network_model import (
    SocialNetworkModel,
    SocialNetworkResponseModel,
)
from services.social_network_service import SocialNetworkService
from utils.auth_manager import get_current_user

router = APIRouter(prefix="/social_network")
service = SocialNetworkService()

@router.post(
    "/",
    response_model=SocialNetworkResponseModel,
    status_code=status.HTTP_201_CREATED,
    summary="Crear red social"
)
async def create_social_network(
    payload: SocialNetworkModel,
    current_user=Depends(get_current_user)
):
    return await service.create(payload, current_user.username)

@router.get(
    "/{username}",
    response_model=List[SocialNetworkResponseModel],
    summary="Listar redes sociales del usuario"
)
async def list_social_networks(username: str):
    return await service.list_by_user(username)

@router.put(
    "/{id}",
    response_model=SocialNetworkResponseModel,
    summary="Actualizar red social"
)
async def update_social_network(
    id: str,
    payload: SocialNetworkModel,
    current_user=Depends(get_current_user)
):
    return await service.update(id, payload, current_user.username)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar red social"
)
async def delete_social_network(
    id: str,
    current_user=Depends(get_current_user)
):
    await service.delete(id, current_user.username)