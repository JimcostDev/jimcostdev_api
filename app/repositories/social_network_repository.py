from motor.motor_asyncio import AsyncIOMotorCollection
from repositories.base_repository import BaseRepository

class SocialNetworkRepository(BaseRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    async def find_by_username(self, username: str) -> list[dict]:
        cursor = self.collection.find({"username": username})
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results