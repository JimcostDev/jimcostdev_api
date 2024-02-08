from pydantic import BaseModel, HttpUrl, Field


class CertificationModel(BaseModel):
    company: str = Field(...,
                         description="La empresa que otorga la certificación")
    certification: str = Field(...,
                               description="El nombre de la certificación")
    link: HttpUrl = Field(..., description="El link de la certificación")

    class Config:
        json_schema_extra = {
            "example": {
                "company": "Google",
                "certification": "Google Cloud Platform",
                "link": "https://www.credly.com/badges/1234567890"
            }
        }


class CertificationResponseModel(BaseModel):
    id: int = Field(..., description="El id de la certificación")
    company: str = Field(...,
                         description="La empresa que otorga la certificación")
    certification: str = Field(...,
                               description="El nombre de la certificación")
    link: HttpUrl = Field(..., description="El link de la certificación")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "company": "Google",
                "certification": "Google Cloud Platform",
                "link": "https://www.credly.com/badges/1234567890"
            }
        }
