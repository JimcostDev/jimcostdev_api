from pydantic import BaseModel, Field, EmailStr, validator, constr
from typing import Optional

class GoogleAuthModel(BaseModel):
    user_id: str

class UserBase(BaseModel):
    """Schema for creating a User."""
    full_name: constr(min_length=2, max_length=50) = Field(..., description="Nombre completo de usuario (entre 2 y 50 caracteres)")
    username: constr(min_length=4, max_length=20) = Field(..., description="Identidicador de usuario (entre 4 y 20 caracteres)")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")
    password: constr(min_length=8)
    confirm_password: constr(min_length=8)
    
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
    full_name: constr(min_length=2, max_length=50) = Field(..., description="Nombre completo de usuario (entre 2 y 50 caracteres)")
    username: constr(min_length=4, max_length=20) = Field(..., description="Nombre de usuario (entre 4 y 20 caracteres)")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")
    password: constr(min_length=8) = None
    confirm_password: constr(min_length=8) = None
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

class UserCreateModel(UserBase):
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Ronaldo Jimenez Acosta",
                "username": "example_user",
                "email": "user@example.com",
                "password": "Password123*",
                "confirm_password": "Password123*",
            }
        }
    
class UserResponseModel(BaseModel):
    id: int = Field(..., description="Identificador único del contacto.")
    full_name: constr(min_length=2, max_length=50) = Field(..., description="Nombre completo de usuario (entre 2 y 50 caracteres)")
    username: constr(min_length=4, max_length=20) = Field(..., description="Identidicador de usuario (entre 4 y 20 caracteres)")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")
    class Config:
        # Excluir campos específicos al crear la instancia de UserResponseModel
        exclude = ["password", "confirm_password"]

class UserInDB(UserResponseModel):
    """Schema for User stored in database."""
    created_at: str = Field(..., description="Fecha de creación del usuario")
    updated_at: str = Field(..., description="Fecha de última actualización del usuario")