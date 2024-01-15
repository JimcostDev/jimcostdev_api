from fastapi import HTTPException, status
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.contact_model import UserCreateModel, UserUpdateModel, UserResponseModel
from utils.generate_id import obtener_ultimo_id
from utils.hash_and_verify_password import hash_password, verify_password
from datetime import datetime


# Verificar si usuario existe por email o username
def user_exists(identifier: str) -> bool:
    db = get_database_instance()
    # Determinar si el identificador parece ser un correo electrónico o un nombre de usuario
    conditions = {}
    if "@" in identifier:  # Si hay un "@" en el identificador, asumimos que es un correo electrónico
        conditions["email"] = {"$regex": f"^{identifier}$", "$options": "i"}
    else:  # En caso contrario, asumimos que es un nombre de usuario
        conditions["username"] = {"$regex": f"^{identifier}$", "$options": "i"}

    existing_user = db.users_collection.find_one(conditions)
    return existing_user is not None
    
# CREAR USUARIO
async def create_user(user_data_data: UserCreateModel):
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        user_data_data (UserCreateModel): Datos del nuevo usuario.

    Returns:
        tuple: Una tupla que contiene el usuario y el código de estado HTTP.
    """
    try:
        user_data = user_data_data.dict(exclude_unset=True)  # Excluir campos no configurados
        user_data['avatar'] = str(user_data['avatar'])  # Convertir la URL a una cadena
        user_data['created_at'] = str(datetime.utcnow())
        user_data['updated_at'] = str(datetime.utcnow())
        user_data['roles'] = ['user'] 
        
        # Excluir el campo 'confirm_password' antes de la inserción
        user_data.pop('confirm_password', None)
    
        # Hashear la contraseña antes de guardarla en la base de datos
        hashed_password = hash_password(user_data_data.password)
        user_data['password'] = hashed_password   
        
    except ValidationError as e:
        # Manejar errores de validación Pydantic aquí
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error de validación: {e.errors()}"
        )

    try:
        # Obtener la instancia de la base de datos
        db = get_database_instance()
        
        # Verificar si el usuario ya existe
        if user_exists(user_data['email']) or user_exists(user_data['username']) :
            return None, status.HTTP_409_CONFLICT  # Retorna None con un código de conflicto si el usuario ya existe
        
        # Obtener el último id de la colección 
        ultimo_id = obtener_ultimo_id(db.users_collection)

        # Asignar el nuevo id al documento 
        user_data["_id"] = ultimo_id

        # Insertar el nuevo usuario en la colección 
        result = db.users_collection.insert_one(user_data)
        
        # Comprobar si la inserción fue exitosa
        if result.inserted_id:
            # Devolver una instancia del modelo y el código de estado 201
            return UserCreateModel(**user_data).dict(), status.HTTP_201_CREATED
        else:
            # Devolver el código de estado 500 si la inserción falla
            return None, status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as ex:
        # Devolver el código de estado 500 y los detalles de la excepción
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al crear el usuario: {str(ex)}"
        )
        
    finally:
        # Asegurarse de cerrar la conexión a la base de datos
        db.close_connection()