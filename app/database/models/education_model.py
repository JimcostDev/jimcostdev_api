from pydantic import BaseModel, Field


class EducationModel(BaseModel):
    company: str = Field(...,
                         description="La empresa que otorga la educación")
    career: str = Field(...,
                        description="El nombre del grado o estudios")
    year: int = Field(..., description="año de graduación", gt=1900, lt=2100)

    class Config:
        json_schema_extra = {
            "example": {
                "company": "UNIR",
                "career": "Ingeniería Informática",
                "year": 2024
            }
        }


class EducationResponseModel(BaseModel):
    id: int = Field(..., description="El id de la educación")
    company: str = Field(...,
                         description="La empresa que otorga la educación")
    career: str = Field(...,
                        description="El nombre del grado o estudios")
    year: int = Field(..., description="año de graduación", gt=1900, lt=2100)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "company": "UNIR",
                "career": "Ingeniería Informática",
                "year": 2024
            }
        }
