from pydantic import BaseModel, Field, HttpUrl
from typing import Union, Optional

class CertificationCreate(BaseModel):
    company: str = Field(..., description="La empresa que otorga la certificación")
    certification: str = Field(..., description="El nombre de la certificación")
    link: HttpUrl = Field(..., description="El link de la certificación")

    model_config = {
        "json_schema_extra": {
            "example": {
                "company": "Google",
                "certification": "Google Cloud Platform",
                "link": "https://www.credly.com/badges/1234567890"
            }
        }
    }

class CertificationResponse(BaseModel):
    id: Union[str, int] = Field(..., description="ID único de la certificación")
    company: str = Field(..., description="La empresa que otorga la certificación")
    certification: str = Field(..., description="El nombre de la certificación")
    link: HttpUrl = Field(..., description="El link de la certificación")
    username: Optional[str] = Field(None, description="Usuario propietario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "company": "Google",
                "certification": "Google Cloud Platform",
                "link": "https://www.credly.com/badges/1234567890",
                "username": "user"
            }
        }
    }