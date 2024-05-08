from pydantic import BaseModel, Field, EmailStr, validator, constr
from typing import Optional

class GoogleAuthModel(BaseModel):
    user_id: str

class UserBase(BaseModel):
    """Schema for creating a User."""
    full_name: str = Field(..., description="Nombre completo de usuario ")
    username: str = Field(..., description="Identidicador de usuario ")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")
    password: str
    confirm_password: str
    
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
    full_name: Optional[str] = Field(None, description="Nombre completo de usuario")
    email: Optional[EmailStr] = Field(None, description="Dirección de correo electrónico")
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    roles: Optional[str] = None
    reset_password_token: Optional[str] = None
    
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

class UserUpdatePasswordModel(BaseModel):
    password: str
    confirm_password: str
    
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
    class Config:
        json_schema_extra = {
            "example": {
                "password": "Cambiar123*",
                "confirm_password": "Cambiar123*"
            }
        }

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
    full_name: str = Field(..., description="Nombre completo de usuario ")
    username: str = Field(..., description="Identidicador de usuario ")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")
    class Config:
        # Excluir campos específicos al crear la instancia de UserResponseModel
        exclude = ["password", "confirm_password"]

class UserInDB(UserResponseModel):
    """Schema for User stored in database."""
    created_at: str = Field(..., description="Fecha de creación del usuario")
    updated_at: str = Field(..., description="Fecha de última actualización del usuario")
    
    
class LoginUser(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword",
            }
        }