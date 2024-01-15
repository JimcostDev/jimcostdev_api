from pydantic import BaseModel, Field, EmailStr, HttpUrl

class WebModel(BaseModel):
    url: HttpUrl = Field(..., description="La URL debe ser una URL válida.")
    name: str = Field(..., description="Tag para la personalización")

class ContactModel(BaseModel):
    avatar: HttpUrl = Field(..., description="URL de la imagen del avatar.")
    nationality:  str = Field(..., description="Tu nacionalidad, longitud entre 1 y 50 caracteres.")
    phone_number: str = Field(..., description="Número de teléfono de contacto.")
    i_live_in: str = Field(..., description="Ubicación actual.")
    email: EmailStr = Field(..., description="Dirección de correo electrónico válida.")
    web: WebModel = Field(..., description="Información relacionada con la web.")
    username: str = Field(..., description="Identificador único de usuario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "avatar": "https://example.com/imgs/perfil.png",
                "nationality": "país",
                "phone_number": "(+34) 624 499234",
                "i_live_in": "lugar donde vives",
                "email": "correo@gmail.com",
                "web": {
                    "url": "https://www.jimcostdev.com/",
                    "name": "jimcostdev.com"
                },
                "username": "username"
            }
        }

class ContactResponseModel(ContactModel):
    id: int = Field(..., description="Identificador único del contacto.", gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "_id": 1,
                "avatar": "https://example.com/imgs/perfil.png",
                "nationality": "país",
                "phone_number": "(+34) 624 499234",
                "i_live_in": "lugar donde vives",
                "email": "correo@gmail.com",
                "web": {
                    "url": "https://www.jimcostdev.com/",
                    "name": "jimcostdev.com"
                },
                "username": "username"
            }
        }