import os
#from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import  HTTPException, status, Depends
from database.operations.user_db import get_user

# Obtener secret_key
#load_dotenv("config.env")
secret_key = os.getenv("JWT_SECRET_KEY")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Instancia del esquema OAuth2

# Función para generar token
def create_token(token_payload: dict, secret_key: str):
    try:
        # Generar el token JWT
        token = jwt.encode(token_payload, secret_key, algorithm='HS256')   
        # Devolver el token en la respuesta
        return {"message": "Inicio de sesión exitoso", "access_token": token, "token_type": "bearer"}  
    
    except Exception as e:
        # Otra excepción
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al generar el token: {e}")
    
# Función para obtener el token JWT y verificarlo
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Verificar el token aquí decodificándolo
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        # Obtener el usuario desde el token
        username: str = payload.get("sub")
        user = get_user(username)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user  
    except jwt.ExpiredSignatureError:
        # Token expirado
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    
    except JWTError as e:
        print(f"Error decodificando el token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"No se pudo validar las credenciales: {e}")

# Función de dependencia para verificar el rol del usuario
def check_user_role(current_user: dict = Depends(get_current_user)):
    # Verificar que el usuario tenga el rol necesario para consultar usuarios
    allowed_roles = ['super-admin', 'admin']
    
    # Obtener el valor de la clave "roles" o un valor predeterminado si la clave no está presente
    user_roles = current_user.get("roles", [])
    
    # Verificar si al menos uno de los roles en user_roles está en allowed_roles
    if not any(role in allowed_roles for role in user_roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin' o 'admin'")

    return current_user
