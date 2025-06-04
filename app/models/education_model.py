from typing import Union, Optional
from pydantic import BaseModel, Field


class EducationCreate(BaseModel):
    company: str = Field(..., description="La empresa que otorga la educación")
    career: str = Field(..., description="El nombre del grado o estudios")
    year: int = Field(..., description="Año de graduación", gt=1900, lt=2100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "company": "UNIR",
                "career": "Ingeniería Informática",
                "year": 2025
            }
        }
    }


class EducationResponse(EducationCreate):
    id: Union[str, int] = Field(..., description="El id de la educación")
    username: Optional[str] = Field(None, description="Usuario propietario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "company": "UNIR",
                "career": "Ingeniería Informática",
                "year": 2025,
                "username": "usuario123"
            }
        }
    }
