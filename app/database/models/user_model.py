from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
import re


class PasswordStrengthCheck:
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
    secret: str = Field(..., description="Palabra secreta para recuperar contraseña (puede ser una frase, el nombre de tu mascota, color favorito, etc.)")
    password: str
    confirm_password: str

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if v != info.data.get('password'):
            raise ValueError('Las contraseñas no coinciden')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        PasswordStrengthCheck.validate_password_strength(v)
        return v


class UserUpdateModel(BaseModel):
    full_name: Optional[str] = Field(None, description="Nombre completo de usuario")
    email: Optional[EmailStr] = Field(None, description="Dirección de correo electrónico")
    secret: Optional[str] = Field(None, description="Palabra secreta para recuperar contraseña (puede ser una frase, el nombre de tu mascota, color favorito, etc.)")
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    roles: Optional[str] = None
    reset_password_token: Optional[str] = None

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if v is not None and v != info.data.get('password'):
            raise ValueError('Las contraseñas no coinciden')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if v is not None:
            PasswordStrengthCheck.validate_password_strength(v)
        return v


class ResetPasswordModel(BaseModel):
    password: Optional[str] = None
    confirm_password: Optional[str] = None

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if v is not None and v != info.data.get('password'):
            raise ValueError('Las contraseñas no coinciden')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if v is not None:
            PasswordStrengthCheck.validate_password_strength(v)
        return v


class UserResponseModel(BaseModel):
    id: int = Field(..., description="Identificador único del contacto.")
    full_name: str = Field(..., description="Nombre completo de usuario ")
    username: str = Field(..., description="Identidicador de usuario ")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")

    model_config = {
        "json_schema_extra": {
            "exclude": ["password", "confirm_password"]
        }
    }


class LoginUser(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword",
            }
        }
    }