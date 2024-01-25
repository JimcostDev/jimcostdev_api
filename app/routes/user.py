from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Path,
    Depends
)
from utils.auth_manager import check_user_role
from database.operations.user_db import (
    create_user,
    user_exists_by_email,
    user_exists_by_username,
    get_user,
    get_user_by_email,
    update_user,
    delete_user
)
from database.models.user_model import (
    UserCreateModel,
    UserResponseModel,
    UserUpdateModel
)
from database.conn_db import get_database_instance
from pydantic import EmailStr
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# crear usuario
@router.post(
    "/users/",
    tags=['users'],
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Este endpoint permite crear un nuevo usuario en la base de datos. "
                "La información del usuario debe ser proporcionada en el cuerpo de la solicitud. "
                "Tras la creación exitosa, retorna un mensaje confirmando que el usuario ha sido creado."
)
def create_user_endpoint(new_user_data: UserCreateModel):
    """
    Crea un nuevo usuario.

    Args:
        new_user_data (UserCreateModel): Datos del nuevo usuario.

    Returns:
        dict: Datos del usuario creado.
    """
    with get_database_instance() as db:
        #Check if user already exists
        if user_exists_by_email(db, new_user_data.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya esta en uso")
            
        if user_exists_by_username(db, new_user_data.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El username ya esta en uso")
            
        try:
            created_user, http_status = create_user(new_user_data)
            
            if http_status == status.HTTP_201_CREATED:
                return created_user
            else:
                raise HTTPException(
                    status_code=http_status,
                    detail=f"Error al crear el usuario. Status Code: {http_status}"
                )
        except HTTPException as e:
            return e
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error inesperado al crear el usuario: {str(ex)}"
            )

# consultar usuario por username
@router.get(
    "/users/{username}", 
    tags=['users'],
    response_model=UserResponseModel,
    summary="Obtener usuario por su nombre",
    description="Este endpoint permite obtener la información detallada del usuario"
)
def get_user_endpoint(username: str = Path(min_length=2, max_length=20)):
    user, http_status = get_user(username)
    
    if http_status == status.HTTP_200_OK:
        return user

    raise HTTPException(
        status_code=http_status,
        detail=f"Error al consultar información de usuario. Status Code: {http_status}"
    )
    
# consultar usuario por email
@router.get(
    "/users/email/{email}", 
    tags=['users'],
    response_model=UserResponseModel,
    summary="Obtener usuario por su email",
    description="Este endpoint permite obtener la información detallada del usuario"
)
def get_userbyEmail_endpoint(email: EmailStr):
    user = get_user_by_email(email)
    
    if  user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar la información del usuario, email: '{email}' no existe.")
    return user


# actualizar usuario
@router.put(
    "/users/{username}",
    tags=['users'],
    summary="Actualizar información de usuario",
    description="Este endpoint permite actualizar la información de un usuario existente en la base de datos. "
                "Proporciona el username del usuario en la URL y la información actualizada en el cuerpo de la solicitud. "
                "Si la actualización es exitosa, retorna la información actualizada del usuario."
)
def update_user_endpoint(username: str, updated_info: UserUpdateModel, current_user: dict = Depends(check_user_role)):
        try:
            # Verificar que el usuario actual esté actualizando su propia información
            if current_user["username"] != username:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para actualizar la información de otro usuario."
                )
            message, http_status = update_user(username, updated_info)

            if http_status == status.HTTP_200_OK:
                return message
            else:
                raise HTTPException(
                    status_code=http_status,
                    detail=f"Error al crear el usuario. Status Code: {http_status}"
                )
        except HTTPException as e:
            logger.error(f"HTTPException: {e.detail}")
            raise e
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error inesperado al actualizar el usuario: {str(ex)}"
            )

# eliminar usuario por su id
@router.delete(
    "/users/{username}",
    tags=['users'],
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario",
    description="Este endpoint permite eliminar un usuario existente en la base de datos.",
)
def delete_user_endpoint(username: str, current_user: dict = Depends(check_user_role)):
        try:
            # Verificar que el usuario actual esté eliminando su propia información
            if current_user["username"] != username:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para eliminar la información de otro usuario."
                )
            message, http_status = delete_user(username)
            if http_status == status.HTTP_200_OK:
                return message 
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el usuario para eliminar")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))