from datetime import datetime, timezone
from core.database import mongodb
from repositories.education_repository import EducationRepository
from models.education_model import (
    EducationCreate,
    EducationResponse
)
from exceptions import (
    NotFoundException,
    ConflictException,
    DatabaseException
)

class EducationService:
    def __init__(self):
        self.repo = None

    async def _init_repo(self):
        if not self.repo:
            coll = await mongodb.get_collection("education")
            self.repo = EducationRepository(coll)
            
    async def list_education(self, username: str) -> list[EducationResponse]:
        await self._init_repo()
        try:
            existing = await self.repo.collection.find_one({"username": username})
            if not existing:
                raise NotFoundException(f"No se encontraron datos para el usuario {username}")
            docs = await self.repo.find_by_username(username)
            return [EducationResponse(**{**d, "id": d.pop("_id")}) for d in docs]
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error listing education") from e
    
    async def get_education(self, id: str, username: str) -> EducationResponse:
        await self._init_repo()
        doc = await self.repo.find_by_id(id)
        if not doc or doc.get("username") != username:
            raise NotFoundException("Education not found")
        # convertir un documento MongoDB en un modelo Pydantic que tiene una propiedad id (en lugar de _id).
        return EducationResponse(**{**doc, "id": doc.pop("_id")})
        
    async def create_education(
        self, payload: EducationCreate, username: str
    ) -> EducationResponse:
        await self._init_repo()
        try:
            existing = await self.repo.collection.find_one({"education": payload.career, "username": username})
            if existing:
                raise ConflictException(f"Education '{payload.career}' already exists for user {username}")
            
            now = datetime.now(timezone.utc).isoformat()
            data = payload.model_dump()
            
            data.update({
            "username": username,
            "created_at": now,
            "updated_at": now
            })
            
            created = await self.repo.create(data)
            return EducationResponse(**{**created, "id": created.pop("_id")})
        except Exception as e:
            raise DatabaseException("Error creating education") from e
        
    async def update_education(
        self, id: str, payload: EducationCreate, username: str
    ) -> EducationResponse:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if doc.get("username") != username:
                raise NotFoundException("Education no pertenece al usuario autenticado")
            
            now = datetime.now(timezone.utc).isoformat()
            data = payload.model_dump(exclude_unset=True)
            
            data.update({
                "updated_at": now
            })
            
            updated = await self.repo.update(id, data)
            return EducationResponse(**{**updated, "id": updated.pop("_id")})
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error updating education") from e
        
    async def delete_education(self, id: str, username: str) -> None:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if not doc or doc.get("username") != username:
                raise NotFoundException("Education no pertenece al usuario autenticado o no existe")
            
            await self.repo.delete(id)
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error deleting education") from e