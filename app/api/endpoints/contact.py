from fastapi import APIRouter, Depends, status
from models.contact_model import (
    ContactCreate,
    ContactResponse
)
from services.contact_service import ContactService
from utils.auth_manager import check_admin_role

router = APIRouter(prefix="/contact")
service = ContactService()

# -- GET públicos con prefijo /p/ --
@router.get(
    "/p/{username}",
    response_model=list[ContactResponse],
    summary="Listar datos de contacto por usuario",
    description="Obtiene todas los datos de contacto de un usuario por su nombre"
)
async def list_contact(username: str):
    return await service.list_contact(username)


# -- Operaciones privadas (POST, PUT, DELETE) --
@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear contacto",
    description="Crea una nueva información de contacto para el usuario autenticado",
)
async def create_contact(
    payload: ContactCreate,
    current_user=Depends(check_admin_role)
):
    return await service.create_contact(payload, current_user.username)

@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ContactResponse,
    summary="Actualizar contacto",
    description="Actualiza un contacto existente del usuario autenticado por su ID",
)
async def update_contact(
    id: str,
    payload: ContactCreate,
    current_user=Depends(check_admin_role)
):
    return await service.update_contact(id, payload, current_user.username)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar contacto",
    description="Elimina un contacto del usuario autenticado por su ID",
)
async def delete_contact(
    id: str,
    current_user=Depends(check_admin_role)
):
    await service.delete_contact(id, current_user.username)