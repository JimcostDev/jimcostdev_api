from typing import Optional
from fastapi import (
    HTTPException, 
    status
)

from pydantic import (
    ValidationError, 
    EmailStr
)

from database.models.user_model import (
    UserCreateModel, 
    UserUpdateModel
)

from database.conn_db import get_database_instance
from utils.generate_id import obtener_ultimo_id
from utils.hash_and_verify_password import hash_password
from datetime import datetime
from pymongo.errors import PyMongoError
import logging

logger = logging.getLogger(__name__)

# verificar si usuario existe
def user_exists_by_email(db, user_email: str) -> bool:
    try:
        existing_user = db.users_collection.find_one({"email": {"$regex": f"^{user_email}$", "$options": "i"}})
        return existing_user is not None
    except PyMongoError as e:
        # Aquí puedes manejar la excepción según tus necesidades
        print(f"Error al buscar usuario en la base de datos: {e}")
        return False

def user_exists_by_username(db, username: str) -> bool:
    try:
        existing_user = db.users_collection.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
        return existing_user is not None
    except PyMongoError as e:
        # Aquí puedes manejar la excepción según tus necesidades
        print(f"Error al buscar usuario en la base de datos: {e}")
        return False

# crear usuario
def create_user(new_user_data: UserCreateModel):
    with get_database_instance() as db:
        try:
            # Validate fields
            user_data = new_user_data.dict(exclude_unset=True)
            
            # Add fields
            user_data['created_at'] = str(datetime.utcnow())
            user_data['updated_at'] = str(datetime.utcnow())
            user_data['roles'] = ['admin']
            
            # Remove 'confirm_password' before insertion and hashed 'password'
            user_data.pop('confirm_password', None)
            hashed_password = hash_password(new_user_data.password)
            user_data['password'] = hashed_password
            
            if user_exists_by_email(db, user_data['email']):
                    return None, status.HTTP_409_CONFLICT
                
            if user_exists_by_username(db, user_data['username']):
                    return None, status.HTTP_409_CONFLICT
            
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Error de validación: {e.errors()}"
            )

        try:
            
            # Get the last id from the collection
            ultimo_id = obtener_ultimo_id(db.users_collection)

            # Assign the new id to the document
            user_data['_id'] = ultimo_id

            # Insert the new user into the collection
            
            result = db.users_collection.insert_one(user_data)
            
            if result.inserted_id:
                # Return the user data along with status code 201
                return {"message": "Usuario creado exitosamente"}, status.HTTP_201_CREATED
            else:
                # Return status code 500 if insertion fails
                return None, status.HTTP_500_INTERNAL_SERVER_ERROR
        except PyMongoError as ex:
            logger.error(f"PyMongoError(): Error al insertar usuario: {ex}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"PyMongoError(): Error inesperado al crear el usuario. {ex}"
            )
        except Exception as ex:
            logger.error(f"Error al insertar usuario: {ex}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error inesperado al crear el usuario. {ex}"
            )

# obtener user por su username
def get_user(username: str) -> dict:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            user = db.users_collection.find_one({"username": username})

            if user:
                user['id'] = user.pop('_id')
                return user
            else:
                #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar la información del usuario, '{username}' no existe.")
                return None
    except Exception as e:
        raise e

# obtener user por su email
def get_user_by_email(email: EmailStr) -> Optional[dict]:
    try:
        # Obtener la instancia de la base de datos
        with get_database_instance() as db:
            user = db.users_collection.find_one({"email": email})

            if user:
                user['id'] = user.pop('_id')
                return user
            else:
                #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar la información del usuario, email: '{email}' no existe.")
                return None
    except Exception as e:
        raise e
    
# actualizar usuario
def update_user(updated_info: UserUpdateModel, username: str):
    with get_database_instance() as db:
        try: 
            existing_user = db.users_collection.find_one({"username": username})

            if existing_user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe.")
                #return {"message": "El usuario no existe."}, status.HTTP_404_NOT_FOUND
           
            # Verificar si el email actualizado ya existe en otro usuario
            if updated_info.email != existing_user['email']:
                if user_exists_by_email(db, updated_info.email):
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"No se pudo actualizar el usuario, el email: '{updated_info.email}' ya está en uso.")
                    #return {"message": f"No se pudo actualizar el usuario, el email: '{updated_info.email}' ya está en uso."}, status.HTTP_404_NOT_FOUND
              
            updated_values = updated_info.dict(exclude_unset=True)
            updated_values['updated_at'] = str(datetime.utcnow())
            # Excluir 'confirm_password' antes de la inserción
            updated_values.pop('confirm_password', None)
            # Excluir 'confirm_password' de updated_info también
            updated_info.dict().pop('confirm_password', None)
                
            # Hashear la contraseña si se actualiza
            if 'password' in updated_values:
                hashed_password = hash_password(updated_values['password'])
                updated_values['password'] = hashed_password
            else:
                # Asegúrate de que la contraseña existente no se modifique
                updated_values.pop('password', None)
                    
            # Actualizar y obtener el resultado
            result = db.users_collection.update_one(
                {"username": username},
                {"$set": updated_values}
            )

            if result.matched_count > 0 and result.modified_count > 0:
                return {"message": "Usuario actualizado exitosamente"}, status.HTTP_200_OK
            else:
                return {"message": "Usuario no encontrado o no se realizó ninguna actualización"}, status.HTTP_404_NOT_FOUND
        
        except HTTPException as he:
            logger.error(f"HTTPException: {he.detail}")
            raise he
    
        except Exception as ex:
            logger.exception(f"Error inesperado al actualizar el usuario: {ex}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error inesperado al actualizar el usuario: {ex}"
            )

# Eliminar usuario
def delete_user(username: str) -> dict:
    with get_database_instance() as db:
        try:
            result = db.users_collection.delete_one({"username": username})
            if result.deleted_count > 0:
                message = {"message": "Usuario eliminado exitosamente"}
                return message, status.HTTP_200_OK
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el usuario para eliminar")
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar usuario: {e}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        