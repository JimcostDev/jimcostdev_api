from pydantic import BaseModel, Field, HttpUrl
from typing import Union, Optional

class SocialNetworkCreate(BaseModel):
    title: str = Field(..., description="Nombre de la red social")
    url: HttpUrl = Field(..., description="URL de la red social")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "linkedin",
                "url": "https://www.linkedin.com/in/usuario"
            }
        }
    }

class SocialNetworkResponse(BaseModel):
    id: Union[str, int] = Field(..., description="ID único de la red social")
    title: str = Field(..., description="Nombre de la red social")
    url: HttpUrl = Field(..., description="URL de la red social")
    username: Optional[str] = Field(None, description="Usuario propietario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "60f7f9a5e1d3a2b4c5d6f7e8",
                "title": "linkedin",
                "url": "https://www.linkedin.com/in/usuario",
                "username": "user"
            }
        }
    }