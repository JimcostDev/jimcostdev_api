from fastapi import APIRouter, Depends
from pydantic import EmailStr
from services.user_service import UserService
from models.user_model import (
    UserModel,
    UserResponseModel,
    UserUpdateModel,
    ResetPasswordModel,
)
from utils.auth_manager import check_admin_role
from exceptions import (
    ConflictException,
    ValidationException,
    DatabaseException,
)

router = APIRouter(prefix="/users")
service = UserService()

@router.post(
    "/",
    response_model=UserResponseModel,
    status_code=201,
    summary="Crear un nuevo usuario",
)
async def create_user_endpoint(new_user: UserModel):
    try:
        return await service.create_user(new_user)
    except (ConflictException, ValidationException) as e:
        raise e
    except Exception as e:
        raise DatabaseException(str(e))

@router.get(
    "/{username}",
    response_model=UserResponseModel,
    summary="Obtener usuario por nombre",
)
async def get_user_endpoint(username: str):
    return await service.get_user(username)

@router.get(
    "/email/{email}",
    response_model=UserResponseModel,
    summary="Obtener usuario por email",
)
async def get_user_by_email_endpoint(email: EmailStr):
    return await service.get_user_by_email(email)

@router.put(
    "/",
    response_model=UserResponseModel,
    summary="Actualizar usuario autenticado",
    dependencies=[Depends(check_admin_role)],
)
async def update_user_endpoint(
    updated_info: UserUpdateModel,
    current_user: dict = Depends(check_admin_role)
):
    username = current_user.username
    return await service.update_authenticated_user(username, updated_info)

@router.put(
    "/reset-password",
    response_model=UserResponseModel,
    summary="Restablecer contraseña",
)
async def reset_password_endpoint(
    updated_info: ResetPasswordModel,
    username: str,
    secret: str,
):
    return await service.reset_password(username, secret, updated_info)

@router.delete(
    "/",
    summary="Eliminar usuario autenticado",
    dependencies=[Depends(check_admin_role)],
)
async def delete_user_endpoint(current_user: dict = Depends(check_admin_role)):
    username = current_user.username
    await service.delete_authenticated_user(username)
    return {"message": "Usuario eliminado exitosamente"}