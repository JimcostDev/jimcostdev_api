from typing import Optional, Union
from pydantic import BaseModel, Field

class WorkExperienceCreate(BaseModel):
    rol: str = Field(..., title="Cargo que desempeña la persona en la empresa")
    company: str = Field(..., title="Nombre de la empresa")
    location: str = Field(..., title="Ubicación de la empresa o lugar de trabajo, puede ser remoto")
    activities: str = Field(..., title="Actividades principales realizadas en el trabajo")
    initial_date: str = Field(..., title="Fecha de inicio de la experiencia laboral (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, title="Fecha de finalización de la experiencia laboral (YYYY-MM-DD)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "rol": "Desarrollador de software",
                "company": "Empresa X",
                "location": "Ciudad X",
                "activities": "Desarrollo de aplicaciones web",
                "initial_date": "2021-01-01",
                "end_date": "2021-12-31"
            }
        }
    }

class WorkExperienceResponse(WorkExperienceCreate):
    id: Union[str, int] = Field(..., title="ID de la experiencia laboral")
    username: Optional[str] = Field(None, title="Usuario propietario")
    duration: Optional[str] = Field(None, title="Duración de la experiencia laboral")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "rol": "Desarrollador de software",
                "company": "Empresa X",
                "location": "Ciudad X",
                "activities": "Desarrollo de aplicaciones web",
                "initial_date": "2021-01-01",
                "end_date": "2021-12-31",
                "username": "username",
                "duration": "1 año y 11 meses"
            }
        }
    }
