from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends
)

from database.models.user_model import LoginUser
from database.operations.user_db import get_user_by_email
from utils.hash_and_verify_password import verify_password
from utils.auth_manager import (
    get_current_user,
    create_token,
    oauth2_scheme,
    token_blacklist
)
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Optional
import logging
import os


logger = logging.getLogger(__name__)
router = APIRouter()

# Obtener secret_key
load_dotenv("config.env")
secret_key = os.getenv("JWT_SECRET_KEY")


# Iniciar sesión (login)
@router.post(
    "/login",
    tags=['auth'],
    summary="Iniciar sesión de usuario",
    description="Endpoint para permitir a los usuarios iniciar sesión. Proporciona las credenciales de usuario en el cuerpo de la solicitud. "
                "Si las credenciales son válidas, devuelve un mensaje de inicio de sesión exitoso."
)
def login(user_data: LoginUser):
    try:
        user = get_user_by_email(user_data.email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar la información del usuario, email: '{user_data.email}' no existe.")
                
        # Verificar contraseña
        if not verify_password(user_data.password, user['password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta")

        # Payload del token JWT con información del usuario (puede incluir el ID, nombre, etc.)
        token_payload = {
            'sub': user['username'],
            'roles': user['roles'],
            # Tiempo de expiración del token (30 minutos)
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }

        message = create_token(token_payload, secret_key)
        return message
    except Exception as e:
        logger.error(f"Ocurrió un error durante el login: {e}")
        raise e

# Cerrar sesión (logout)
@router.post(
    "/logout",
    tags=['auth'],
    summary="Cerrar sesión",
    description="Endpoint para cerrar sesión. Invalida el token actual, agregándolo a la lista negra."
)
def logout(current_user: dict = Depends(get_current_user), token: Optional[str] = Depends(oauth2_scheme)):
    try:
        # Agregar el token actual a la lista negra
        if token:
            token_blacklist.add(token)

        return {"message": "Logout exitoso"}
    except Exception as e:
        # Loggear la excepción
        logger.error(f"Ocurrió un error durante el logout: {e}")
        # Levantar una excepción HTTP con un mensaje amigable
        raise HTTPException(
            status_code=500, detail="Error interno del servidor")
