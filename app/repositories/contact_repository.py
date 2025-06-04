from motor.motor_asyncio import AsyncIOMotorCollection
from repositories.base_repository import BaseRepository


class ContactRepository(BaseRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)
