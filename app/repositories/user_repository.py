from motor.motor_asyncio import AsyncIOMotorCollection
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    async def find_by_username(self, username: str) -> dict:
        document = await self.collection.find_one({"username": username})
        if not document:
            return None
        document["_id"] = str(document["_id"])
        return document

    async def find_by_email(self, email: str) -> dict:
        document = await self.collection.find_one({"email": email})
        if not document:
            return None
        document["_id"] = str(document["_id"])
        return document

    async def create_user(self, user_data: dict) -> dict:
        result = await self.collection.insert_one(user_data)
        return await self.find_by_id(str(result.inserted_id))

    async def update_user(self, id: str, update_data: dict) -> dict:
        return await self.update(id, update_data)

    async def delete_user(self, id: str) -> bool:
        return await self.delete(id)