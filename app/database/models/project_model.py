from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class ProjectModel(BaseModel):
    image: HttpUrl = Field(..., description="URL de la imagen del proyecto")
    title: str = Field(..., description="Título del proyecto")
    description: str = Field(..., description="Descripción del proyecto")
    stack: Optional[List[str]] = Field(None, description="Lista de tecnologías utilizadas en el proyecto")
    link: Optional[HttpUrl] = Field(None, description="URL del proyecto")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image": "https://jimcostdev-api.azurewebsites.net/assets/images/projects/1.png",
                "title": "Mi proyecto",
                "description": "Descripción de mi proyecto",
                "stack": ["python", "fastapi", "pydantic", "mongodb"],
                "link": "https://jimcostdev-api.azurewebsites.net/projects/1"}
        }

class ProjectResponseModel(BaseModel):
    id: int = Field(..., description="ID del proyecto")
    image: HttpUrl = Field(..., description="URL de la imagen del proyecto")
    title: str = Field(..., description="Título del proyecto")
    description: str = Field(..., description="Descripción del proyecto")
    stack: Optional[List[str]] = Field(None, description="Lista de tecnologías utilizadas en el proyecto")
    link: Optional[HttpUrl] = Field(None, description="URL del proyecto")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "image": "https://jimcostdev-api.azurewebsites.net/assets/images/projects/1.png",
                "title": "Mi proyecto",
                "description": "Descripción de mi proyecto",
                "stack": ["python", "fastapi", "pydantic", "mongodb"],
                "link": "https://jimcostdev-api.azurewebsites.net/projects/1"}
        }