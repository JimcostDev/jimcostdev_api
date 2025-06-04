from motor.motor_asyncio import AsyncIOMotorCollection
from repositories.base_repository import BaseRepository


class SocialNetworkRepository(BaseRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)
