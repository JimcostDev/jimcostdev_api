from pydantic import BaseModel, HttpUrl, Field

class SocialNetworkModel(BaseModel):
    title: str = Field(..., title="Nombre de la red social")
    url: HttpUrl = Field(..., title="URL de la red social")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "linkedin",
                "url": "https://www.linkedin.com/in/ronaldo-jimenez"
            }
        }

class SocialNetworkResponseModel(BaseModel):
    id: int = Field(..., title="ID de la red social")
    title: str = Field(..., title="Nombre de la red social")
    url: HttpUrl = Field(..., title="URL de la red social")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "linkedin",
                "url": "https://www.linkedin.com/in/ronaldo-jimenez"
            }
        }
    