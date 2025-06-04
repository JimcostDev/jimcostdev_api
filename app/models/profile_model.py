from typing import List, Optional, Union
from pydantic import BaseModel, HttpUrl, Field


class ProfileCreate(BaseModel):
    rol: str = Field(..., description="Nombre del rol o cargo")
    description: str = Field(..., description="Descripción de tu perfil como profesional")
    skills: Optional[List[str]] = Field(None, description="Lista de habilidades que posees")
    avatar: HttpUrl = Field(..., description="URL de tu foto de perfil")

    model_config = {
        "json_schema_extra": {
            "example": {
                "rol": "Desarrollador Full-Stack",
                "descripcion": "Soy un desarrollador Full Stack con experiencia en desarrollo web. Me encanta trabajar con tecnologías modernas y aprender cosas nuevas. Soy autodidacta y me gusta trabajar en equipo.",
                "skills": ["python", "fastapi", "astro", "mongodb", "sql"],
                "avatar": "https://avatars.githubusercontent.com/u/53100460?v=4"
            }
        }
    }


class ProfileResponse(ProfileCreate):
    id: Union[str, int] = Field(..., description="El id del perfil")
    username: Optional[str] = Field(None, description="Usuario propietario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "665f89c6e5a4bfa61f0e0b91",
                "rol": "Desarrollador Full Stack",
                "descripcion": "Soy un desarrollador Full Stack con experiencia en desarrollo web. Me encanta trabajar con tecnologías modernas y aprender cosas nuevas. Soy autodidacta y me gusta trabajar en equipo.",
                "skills": ["python", "fastapi", "astro", "mongodb", "sql"],
                "avatar": "https://avatars.githubusercontent.com/u/53100460?v=4",
                "username": "usuario123"
            }
        }
    }
