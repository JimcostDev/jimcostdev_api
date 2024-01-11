from pymongo import MongoClient
from pydantic import BaseModel, EmailStr, HttpUrl

class WebModel(BaseModel):
    url: HttpUrl
    name: str

class ContactModel(BaseModel):
    _id: int
    avatar: HttpUrl  
    nationality: str
    phone_number: str
    i_live_in: str
    email: EmailStr
    web: WebModel
