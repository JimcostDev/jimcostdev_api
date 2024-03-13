from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class PerfilModel(BaseModel):
   rol: str = Field(..., description="Nombre del rol o cargo")
   descripcion: str = Field(..., description="Descripción de tu perfil como profesional")
   skills: Optional[List[str]] = Field(None, description="Lista de habilidades que posees")
   avatar: HttpUrl = Field(..., description="URL de tu foto de perfil")
   
   class Config:
       json_schema_extra = {
           "example": {
               "rol": "Desarrollador Full-Stack",
               "descripcion": "Soy un desarrollador Full Stack con experiencia en desarrollo web. Me encanta trabajar con tecnologías modernas y aprender cosas nuevas. Soy autodidacta y me gusta trabajar en equipo.",
               "skills": ["python", "fastapi", "react", "mongodb", "sql"],
               "avatar": "https://avatars.githubusercontent.com/u/53100460?v=4"
           }
       }
       


class PerfilResponseModel(BaseModel):
    id: int = Field(..., description="El id del perfil")
    rol: str = Field(..., description="Nombre del rol o cargo")
    descripcion: str = Field(..., description="Descripción de tu perfil como profesional")
    skills: List[str] = Field(..., description="Lista de habilidades que posees")
    avatar: HttpUrl = Field(..., description="URL de tu foto de perfil")
    
    class Config:
       json_schema_extra = {
           "example": {
               "id": 1,
               "rol": "Desarrollador Full Stack",
               "descripcion": "Soy un desarrollador Full Stack con experiencia en desarrollo web. Me encanta trabajar con tecnologías modernas y aprender cosas nuevas. Soy autodidacta y me gusta trabajar en equipo.",
               "skills": ["python", "fastapi", "react", "mongodb", "sql"],
               "avatar": "https://avatars.githubusercontent.com/u/53100460?v=4"
           }
       }
    
   
   