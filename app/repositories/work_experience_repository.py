# work_experience_repository.py
from motor.motor_asyncio import AsyncIOMotorCollection
from repositories.base_repository import BaseRepository
from bson import ObjectId
from typing import Union, List, Dict


class WorkExperienceRepository(BaseRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    async def find_by_username(
        self, username: str
    ) -> List[Dict]:
        """
        Devuelve todos los documentos de experiencia laboral del usuario,
        ordenados por initial_date descendente.
        """
        cursor = self.collection.find({"username": username}).sort("initial_date", -1)
        return [doc async for doc in cursor]

    async def find_by_id(
        self, id: Union[str, int]
    ) -> Dict | None:
        """
        Busca un documento por su _id. Acepta legacy (int) o nuevo (str ObjectId).
        """
        if isinstance(id, int) or (isinstance(id, str) and id.isdigit()):
            filtro = {"_id": int(id)}
        else:
            filtro = {"_id": ObjectId(id)}

        return await self.collection.find_one(filtro)

    
