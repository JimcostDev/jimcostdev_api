from pydantic import BaseModel, Field, EmailStr, HttpUrl, validator, constr
from typing import Optional

class GoogleAuthModel(BaseModel):
    user_id: str

class UserCreateModel(BaseModel):
    """Schema for creating a User."""
    username: constr(min_length=4, max_length=20) = Field(..., description="Nombre de usuario (entre 4 y 20 caracteres)")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")
    password: constr(min_length=8)
    confirm_password: constr(min_length=8)
    avatar: HttpUrl = Field(..., description="URL de la imagen o avatar del usuario")
    google_auth: Optional[GoogleAuthModel]  # Propiedad para almacenar información de autenticación de Google
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Las contraseñas no coinciden')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('La contraseña debe contener al menos una letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not any(c in '!@#$%^&*:' for c in v):
            raise ValueError('La contraseña debe contener al menos un carácter especial')
        return v
    
class UserUpdateModel(BaseModel):
    username: constr(min_length=4, max_length=20) = Field(..., description="Nombre de usuario (entre 4 y 20 caracteres)")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")
    password: constr(min_length=8) = None
    confirm_password: constr(min_length=8) = None
    avatar: HttpUrl = Field(..., description="URL de la imagen o avatar del usuario")
    roles: str = None
    reset_password_token: str = None  #propiedad para el token de restablecimiento de contraseña
    
    @validator('confirm_password', pre=True, always=True)
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Las contraseñas no coinciden')
        return v

    @validator('password', pre=True, always=True)
    def validate_password(cls, v):
        if v is not None:
            if not any(c.isupper() for c in v):
                raise ValueError('La contraseña debe contener al menos una letra mayúscula')
            if not any(c.islower() for c in v):
                raise ValueError('La contraseña debe contener al menos una letra minúscula')
            if not any(c.isdigit() for c in v):
                raise ValueError('La contraseña debe contener al menos un número')
            if not any(c in '!@#$%^&*:' for c in v):
                raise ValueError('La contraseña debe contener al menos un carácter especial')
        return v

class UserResponseModel(UserCreateModel):
    id: int = Field(..., description="Identificador único del contacto.", gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "example_user",
                "email": "user@example.com",
                "avatar": "https://example.com/avatar.jpg"
            }
        }

class UserInDB(UserResponseModel):
    """Schema for User stored in database."""
    created_at: str = Field(..., description="Fecha de creación del usuario")
    updated_at: str = Field(..., description="Fecha de última actualización del usuario")