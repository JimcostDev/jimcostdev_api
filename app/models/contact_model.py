from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union

class ContactCreate(BaseModel):
    nationality: str = Field(..., description="Tu nacionalidad, longitud")
    phone_number: str = Field(..., description="Número de teléfono de contacto.")
    i_live_in: str = Field(..., description="Ubicación actual.")
    email: EmailStr = Field(..., description="Correo electrónico del usuario.")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "nationality": "país",
                "phone_number": "(+34) 624 499234",
                "i_live_in": "lugar donde vives"
            }
        }
    }

class ContactResponse(ContactCreate):
    id: Union[str, int] = Field(..., description="Identificador único del contacto.")
    username: Optional[str] = Field(None, description="Usuario propietario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "nationality": "país",
                "phone_number": "(+34) 624 499234",
                "i_live_in": "lugar donde vives",
                "email": "correo@gmail.com",
                "username": "username"
            }
        }
    }