from datetime import datetime, timezone
from core.database import mongodb
from repositories.certification_repository import CertificationRepository
from models.certification_model import (
    CertificationCreate,
    CertificationResponse
)
from exceptions import (
    NotFoundException,
    ConflictException,
    DatabaseException
)

class CertificationService:
    def __init__(self):
        self.repo = None

    async def _init_repo(self):
        if not self.repo:
            coll = await mongodb.get_collection("certifications")
            self.repo = CertificationRepository(coll)
    
    async def list_certifications(self, username: str) -> list[CertificationResponse]:
        await self._init_repo()
        try:
            existing = await self.repo.collection.find_one({"username": username})
            if not existing:
                raise NotFoundException(f"No se encontraron datos para el usuario {username}")
            docs = await self.repo.find_by_username(username)
            return [CertificationResponse(**{**d, "id": d.pop("_id")}) for d in docs]
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error listing certifications") from e
        
    async def get_certification(self, id: str, username: str) -> CertificationResponse:
        await self._init_repo()
        doc = await self.repo.find_by_id(id)
        if not doc or doc.get("username") != username:
            raise NotFoundException("Certification not found")
        # convertir un documento MongoDB en un modelo Pydantic que tiene una propiedad id (en lugar de _id).
        return CertificationResponse(**{**doc, "id": doc.pop("_id")})
    
    async def create_certification(
        self, payload: CertificationCreate, username: str
    ) -> CertificationResponse:
        await self._init_repo()
        try:
            existing = await self.repo.collection.find_one({"certification": payload.certification, "username": username})
            if existing:
                raise ConflictException(f"Certification '{payload.certification}' already exists for user {username}")
            
            now = datetime.now(timezone.utc).isoformat()
            data = payload.model_dump()
            # Convertir HttpUrl a cadena para almacenamiento
            data['link'] = str(data['link'])
            data.update({
            "username": username,
            "created_at": now,
            "updated_at": now
            })
            
            created = await self.repo.create(data)
            return CertificationResponse(**{**created, "id": created.pop("_id")})
        except Exception as e:
            raise DatabaseException("Error creating certification") from e
        
    async def update_certification(
        self, id: str, payload: CertificationCreate, username: str
    ) -> CertificationResponse:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if doc.get("username") != username:
                raise NotFoundException("Certificación no pertenece al usuario autenticado")
            
            now = datetime.now(timezone.utc).isoformat()
            data = payload.model_dump(exclude_unset=True)
            # Convertir HttpUrl a cadena para almacenamiento
            if "link" in data:
                data['link'] = str(data['link'])
            data.update({
                "updated_at": now
            })
            
            updated = await self.repo.update(id, data)
            return CertificationResponse(**{**updated, "id": updated.pop("_id")})
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error updating certification") from e
        
    async def delete_certification(self, id: str, username: str) -> None:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if not doc or doc.get("username") != username:
                raise NotFoundException("Certificación no pertenece al usuario autenticado o no existe")
            
            await self.repo.delete(id)
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error deleting certification") from e