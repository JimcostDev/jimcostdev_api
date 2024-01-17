from fastapi import HTTPException, status
from fastapi.exceptions import ResponseValidationError
from pydantic import ValidationError
from database.conn_db import get_database_instance
from database.models.user_model import UserCreateModel
from utils.generate_id import obtener_ultimo_id
from utils.hash_and_verify_password import hash_password
from datetime import datetime
from pymongo.errors import PyMongoError

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

def create_user(new_user_data: UserCreateModel):
    with get_database_instance() as db:
        try:
            # Validate fields
            user_data = new_user_data.dict(exclude_unset=True)
            
            # Add fields
            user_data['created_at'] = str(datetime.utcnow())
            user_data['updated_at'] = str(datetime.utcnow())
            user_data['roles'] = ['user']
            
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
                return new_user_data.dict(), status.HTTP_201_CREATED
            else:
                # Return status code 500 if insertion fails
                return None, status.HTTP_500_INTERNAL_SERVER_ERROR
        except PyMongoError as ex:
            print(f"PyMongoError(): Error al insertar usuario: {ex}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"PyMongoError(): Error inesperado al crear el usuario. {ex}"
            )
        except Exception as ex:
            print(f"Error al insertar usuario: {ex}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error inesperado al crear el usuario. {ex}"
            )
