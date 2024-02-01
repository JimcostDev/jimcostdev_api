from pydantic import BaseModel, EmailStr, Field

class ContactModel(BaseModel):
    nationality:  str = Field(..., description="Tu nacionalidad, longitud entre 1 y 50 caracteres.")
    phone_number: str = Field(..., description="Número de teléfono de contacto.")
    i_live_in: str = Field(..., description="Ubicación actual.")
    
    
    class Config:
        json_schema_extra = {
            "example": {
                "nationality": "país",
                "phone_number": "(+34) 624 499234",
                "i_live_in": "lugar donde vives"
            }
        }

class ContactResponseModel(ContactModel):
    id: int = Field(..., description="Identificador único del contacto.", gt=0)
    email: EmailStr = Field(..., description="Correo electrónico del usuario.")

    class Config:
        json_schema_extra = {
            "example": {
                "_id": 1,
                "nationality": "país",
                "phone_number": "(+34) 624 499234",
                "i_live_in": "lugar donde vives",
                "email": "correo@gmail.com",
                "username": "username"
            }
        }

