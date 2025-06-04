from fastapi import APIRouter, HTTPException, status
from models.user_model import LoginUser
from utils.hash_and_verify_password import verify_password
from core.database import mongodb
from repositories.user_repository import UserRepository
from utils.auth_manager import create_token  
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth")

# Obtener secret_key desde env
env_secret = os.getenv("JWT_SECRET_KEY")
if not env_secret:
    raise RuntimeError("JWT_SECRET_KEY no configurado en variables de entorno")
secret_key = env_secret

@router.post(
    "/login",
    summary="Iniciar sesión de usuario",
    response_model=dict
)
async def login(user_data: LoginUser):  
    try:
        # Obtener colección con await
        users_collection = await mongodb.get_collection("users")
        repo = UserRepository(users_collection)
        
        # Buscar usuario por email
        user = await repo.find_by_email(user_data.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email no registrado"
            )
            
        # Verificar contraseña con await
        if not await verify_password(user_data.password, user.get("password")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )

        # Usar la nueva función create_token que incluye username en el token
        token_data = await create_token(user)
        return token_data
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )