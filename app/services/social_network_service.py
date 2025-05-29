from core.database import mongodb
from repositories.social_network_repository import SocialNetworkRepository
from models.social_network_model import (
    SocialNetworkModel,
    SocialNetworkResponseModel,
)
from exceptions import (
    NotFoundException,
    DatabaseException
)
from datetime import datetime, timezone

class SocialNetworkService:
    def __init__(self):
        collection = mongodb.get_collection("social_networks")
        self.repo = SocialNetworkRepository(collection)

    async def create(self, payload: SocialNetworkModel, username: str) -> SocialNetworkResponseModel:
        try:
            data = payload.model_dump()
            data.update({
                "username": username,
                "created_at": datetime.now(timezone.utc).isoformat()
            })
            created = await self.repo.create(data)
            return SocialNetworkResponseModel(**{**created, "id": created.pop("_id")})
        except Exception as e:
            raise DatabaseException(str(e))

    async def list_by_user(self, username: str) -> list[SocialNetworkResponseModel]:
        try:
            docs = await self.repo.find_by_username(username)
            return [SocialNetworkResponseModel(**{**doc, "id": doc.pop("_id")}) for doc in docs]
        except Exception as e:
            raise DatabaseException(str(e))

    async def update(self, id: str, payload: SocialNetworkModel, username: str) -> SocialNetworkResponseModel:
        try:
            # Ensure belongs to user
            doc = await self.repo.find_by_id(id)
            if doc.get("username") != username:
                raise NotFoundException("Recurso no encontrado")
            data = payload.model_dump()
            updated = await self.repo.update(id, data)
            return SocialNetworkResponseModel(**{**updated, "id": updated.pop("_id")})
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(str(e))

    async def delete(self, id: str, username: str) -> None:
        try:
            doc = await self.repo.find_by_id(id)
            if doc.get("username") != username:
                raise NotFoundException("Recurso no encontrado")
            await self.repo.delete(id)
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(str(e))