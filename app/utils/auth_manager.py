import os
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from exceptions import NotFoundException
from datetime import datetime, timedelta, timezone
from typing import Dict, Any

# Obtener secret_key desde entorno
env_secret = os.getenv("JWT_SECRET_KEY")
if not env_secret:
    raise RuntimeError("JWT_SECRET_KEY no configurado en variables de entorno")
secret_key = env_secret

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # Endpoint de login

# Función para generar token
async def create_token(user_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Crea un token JWT con la información del usuario
    
    Args:
        user_data: Diccionario con datos del usuario (debe contener username, id y roles)
    
    Returns:
        Dict con access_token y token_type
    """
    try:
        # Construir payload con información esencial
        token_payload = {
            "sub": user_data["username"],
            "id": str(user_data["_id"]),  # Asegurar que el ID es string
            "roles": user_data.get("roles", []),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)  # Expira en 30 minutos
        }
        
        token = jwt.encode(token_payload, secret_key, algorithm='HS256')
        return {"access_token": token, "token_type": "bearer"}
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falta información esencial en el usuario: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar el token: {str(e)}"
        )

# Función para obtener el usuario actual desde el token
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Obtiene el usuario actual a partir del token JWT
    
    Args:
        token: Token JWT obtenido del header Authorization
    
    Returns:
        Diccionario con los datos del usuario
    """
    try:
        # Decodificar el token
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Obtener username del usuario
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: no contiene username de usuario"
            )
        
        from services.user_service import UserService
        user_service = UserService()
        
        # Obtener usuario por ID
        user = await user_service.get_user(username)
        return user
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}"
        )
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

# Función de dependencia para verificar roles
async def check_admin_role(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Verifica que el usuario tenga rol de admin
    
    Args:
        current_user: Datos del usuario obtenidos del token
    
    Returns:
        Datos del usuario si tiene permiso
    """
    allowed_roles = ['super-admin', 'admin']
    user_roles = current_user.roles or []
    if not any(role in allowed_roles for role in user_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permiso denegado. Se requiere rol de administrador"
        )
    
    return current_user

