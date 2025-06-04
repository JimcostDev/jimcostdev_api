from datetime import datetime, timezone
from core.database import mongodb
from repositories.contact_repository import ContactRepository
from models.contact_model import (
    ContactCreate,
    ContactResponse
)
from exceptions import (
    NotFoundException,
    ConflictException,
    DatabaseException
)

class ContactService:
    def __init__(self):
        self.repo = None

    async def _init_repo(self):
        if not self.repo:
            coll = await mongodb.get_collection("contact")
            self.repo = ContactRepository(coll)
            
    async def list_contact(self, username: str) -> list[ContactResponse]:
        await self._init_repo()
        try:
            existing = await self.repo.collection.find_one({"username": username})
            if not existing:
                raise NotFoundException(f"No se encontraron datos para el usuario {username}")
            docs = await self.repo.find_by_username(username)
            return [ContactResponse(**{**d, "id": d.pop("_id")}) for d in docs]
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error listing contact") from e
        
    async def create_contact(
        self, payload: ContactCreate, username: str
    ) -> ContactResponse:
        await self._init_repo()
        try:
            existing = await self.repo.collection.find_one({"contact": payload.email, "username": username})
            if existing:
                raise ConflictException(f"Contacto '{payload.email}' already exists for user {username}")
            
            now = datetime.now(timezone.utc).isoformat()
            data = payload.model_dump()
            
            data.update({
            "username": username,
            "created_at": now,
            "updated_at": now
            })
            
            created = await self.repo.create(data)
            return ContactResponse(**{**created, "id": created.pop("_id")})
        except Exception as e:
            raise DatabaseException("Error creating contact") from e
        
    async def update_contact(
        self, id: str, payload: ContactCreate, username: str
    ) -> ContactResponse:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if doc.get("username") != username:
                raise NotFoundException("Contacto no pertenece al usuario autenticado")
            
            now = datetime.now(timezone.utc).isoformat()
            data = payload.model_dump(exclude_unset=True)
            
            data.update({
                "updated_at": now
            })
            
            updated = await self.repo.update(id, data)
            return ContactResponse(**{**updated, "id": updated.pop("_id")})
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error updating contact") from e
        
    async def delete_contact(self, id: str, username: str) -> None:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if not doc or doc.get("username") != username:
                raise NotFoundException("Contacto no pertenece al usuario autenticado o no existe")
            
            await self.repo.delete(id)
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error deleting contact") from e