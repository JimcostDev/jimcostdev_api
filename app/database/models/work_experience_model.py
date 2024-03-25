from typing import Optional
from pydantic import BaseModel, Field

class WorkExperienceModel(BaseModel):
    rol: str = Field(..., title="Cargo que desempeñó")
    company: str = Field(..., title="Nombre de la empresa")
    location: str = Field(..., title="Ubicación de la empresa o lugar de trabajo, puede ser remoto")
    activities: str = Field(..., title="Actividades principales realizadas en el trabajo")
    initial_date: str = Field(..., title="Fecha de inicio de la experiencia laboral")
    end_date: Optional[str] = Field(None, title="Fecha de finalización de la experiencia laboral")

    class Config:
        json_schema_extra = {
            "example": {
                "rol": "Desarrollador de software",
                "company": "Empresa X",
                "location": "Ciudad X",
                "activities": "Desarrollo de aplicaciones web",
                "initial_date": "2021-01-01",
                "end_date": "2021-12-31"
            }
        }

class WorkExperienceResponseModel(BaseModel):
    id: int = Field(..., title="ID de la experiencia laboral")
    rol: str = Field(..., title="Cargo que desempeñó")
    company: str = Field(..., title="Nombre de la empresa")
    location: str = Field(..., title="Ubicación de la empresa o lugar de trabajo, puede ser remoto")
    activities: str = Field(..., title="Actividades principales realizadas en el trabajo")
    initial_date: str = Field(..., title="Fecha de inicio de la experiencia laboral")
    end_date: Optional[str] = Field(None, title="Fecha de finalización de la experiencia laboral")
    duration: Optional[str] = Field(None, title="Duración de la experiencia laboral")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "rol": "Desarrollador de software",
                "company": "Empresa X",
                "location": "Ciudad X",
                "activities": "Desarrollo de aplicaciones web",
                "initial_date": "2021-01-01",
                "end_date": "2021-12-31",
                "duration": "1 año y 11 meses"
            }
        }

