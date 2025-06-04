from motor.motor_asyncio import AsyncIOMotorCollection
from repositories.base_repository import BaseRepository
from exceptions import (
    NotFoundException,
    DatabaseException
)


class ProfileRepository(BaseRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)
        
    async def add_skill(self, skill: str, username: str) -> dict:
        try:
            result = await self.collection.update_one(
                {"username": username},
                {"$push": {"skills": skill}}
            )
            if result.modified_count == 0:
                raise DatabaseException("Error al agregar la habilidad")
            return {"message": "Habilidad agregada exitosamente"}
        except Exception as e:
            raise DatabaseException(f"Excepción al agregar habilidad: {str(e)}")
        
    async def remove_skill(self, skill: str, username: str) -> dict:
        try:
            exists = await self.collection.find_one({"username": username, "skills": skill})
            if not exists:
                raise NotFoundException("La habilidad no existe en el perfil")

            result = await self.collection.update_one(
                {"username": username},
                {"$pull": {"skills": skill}}
            )
            if result.modified_count == 0:
                raise DatabaseException("Error al remover la habilidad")
            return {"message": "Habilidad removida exitosamente"}
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Excepción al remover habilidad: {str(e)}")
