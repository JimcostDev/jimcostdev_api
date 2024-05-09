from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
import re


class PasswordStrengthCheck(BaseModel):
    @staticmethod
    def validate_password_strength(password: str):
        if len(password) < 8:
            raise ValueError('La contraseña debe contener al menos 8 caracteres')
        if not any(c.isupper() for c in password):
            raise ValueError(
                'La contraseña debe contener al menos una letra mayúscula')
        if not any(c.islower() for c in password):
            raise ValueError(
                'La contraseña debe contener al menos una letra minúscula')
        if not any(c.isdigit() for c in password):
            raise ValueError('La contraseña debe contener al menos un número')
        if not re.search(r'[!@#$%^&*:]', password):
            raise ValueError(
                'La contraseña debe contener al menos un carácter especial')


class UserModel(BaseModel):
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
        PasswordStrengthCheck.validate_password_strength(v)
        return v


class UserUpdateModel(BaseModel):
    full_name: Optional[str] = Field(
        None, description="Nombre completo de usuario")
    email: Optional[EmailStr] = Field(
        None, description="Dirección de correo electrónico")
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    roles: Optional[str] = None
    reset_password_token: Optional[str] = None

    @validator('confirm_password', pre=True, always=True)
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Las contraseñas no coinciden')
        return v

    @validator('password')
    def validate_password(cls, v):
        PasswordStrengthCheck.validate_password_strength(v)
        return v


class UserResponseModel(BaseModel):
    id: int = Field(..., description="Identificador único del contacto.")
    full_name: str = Field(..., description="Nombre completo de usuario ")
    username: str = Field(..., description="Identidicador de usuario ")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")

    class Config:
        # Excluir campos específicos al crear la instancia de UserResponseModel
        exclude = ["password", "confirm_password"]


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
