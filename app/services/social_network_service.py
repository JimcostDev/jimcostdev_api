from datetime import datetime, timezone
from core.database import mongodb
from repositories.social_network_repository import SocialNetworkRepository
from models.social_network_model import (
    SocialNetworkCreate,
    SocialNetworkResponse
)
from exceptions import (
    NotFoundException,
    ConflictException,
    DatabaseException
)

class SocialNetworkService:
    def __init__(self):
        self.repo = None

    async def _init_repo(self):
        if not self.repo:
            coll = await mongodb.get_collection("social_networks")
            self.repo = SocialNetworkRepository(coll)

    async def list_social_networks(self, username: str) -> list[SocialNetworkResponse]:
        await self._init_repo()
        docs = await self.repo.find_by_username(username)
        return [SocialNetworkResponse(**{**d, "id": d.pop("_id")}) for d in docs]

    async def get_social_network(self, id: str, username: str) -> SocialNetworkResponse:
        await self._init_repo()
        doc = await self.repo.find_by_id(id)
        if doc.get("username") != username:
            raise NotFoundException("Social network no pertenece al usuario autenticado")
        return SocialNetworkResponse(**{**doc, "id": doc.pop("_id")})

    async def create_social_network(
        self, payload: SocialNetworkCreate, username: str
    ) -> SocialNetworkResponse:
        await self._init_repo()
        existing = await self.repo.collection.find_one({"title": payload.title, "username": username})
        if existing:
            raise ConflictException(f"Social network '{payload.title}' already exists for user {username}")

        now = datetime.now(timezone.utc).isoformat()
        data = payload.model_dump()
        # Convertir HttpUrl a cadena para almacenamiento
        data['url'] = str(data['url'])
        data.update({
            "username": username,
            "created_at": now,
            "updated_at": now
        })

        created = await self.repo.create(data)
        return SocialNetworkResponse(**{**created, "id": created.pop("_id")})

    async def update_social_network(
        self, id: str, payload: SocialNetworkCreate, username: str
    ) -> SocialNetworkResponse:
        await self._init_repo()
        doc = await self.repo.find_by_id(id)
        if doc.get("username") != username:
            raise NotFoundException("Social network no pertenece al usuario autenticado")

        data = payload.model_dump(exclude_unset=True)
        # Convertir HttpUrl a cadena si se actualiza
        if "url" in data:
            data["url"] = str(data["url"])
        data["updated_at"] = datetime.now(timezone.utc).isoformat()

        updated = await self.repo.update(id, data)
        return SocialNetworkResponse(**{**updated, "id": updated.pop("_id")})

    async def delete_social_network(self, id: str, username: str) -> None:
        await self._init_repo()
        doc = await self.repo.find_by_id(id)
        if doc.get("username") != username:
            raise NotFoundException("Social network no pertenece al usuario autenticado")
        await self.repo.delete(id)