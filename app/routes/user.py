from fastapi import APIRouter, HTTPException, status
from database.operations.user_db import create_user, user_exists_by_email, user_exists_by_username
from database.models.user_model import UserCreateModel
from database.conn_db import get_database_instance

router = APIRouter()

# CREAR USUARIO
@router.post(
    "/users/",
    response_model=UserCreateModel,
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
            print(created_user, http_status)
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