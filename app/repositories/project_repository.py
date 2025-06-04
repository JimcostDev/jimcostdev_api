from motor.motor_asyncio import AsyncIOMotorCollection
from repositories.base_repository import BaseRepository
from exceptions import (
    NotFoundException,
    DatabaseException
)
from bson import ObjectId
from typing import Union


class ProjectRepository(BaseRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    async def add_skill(self, skill: str, id: Union[str, int], username: str) -> dict:
        """
        Agrega una habilidad al campo 'stack' del proyecto identificado por `id` y `username`.
        Acepta tanto `id` int (legacy) como str con ObjectId (nuevo).
        """
        try:
            # 1) Determinar el filtro según el tipo de id
            if isinstance(id, int) or (isinstance(id, str) and id.isdigit()):
                filtro = {"_id": int(id), "username": username}
            else:
                filtro = {"_id": ObjectId(id), "username": username}

            # 2) Verificar que el proyecto existe
            doc = await self.collection.find_one(filtro)
            if doc is None:
                raise NotFoundException("Proyecto no encontrado para el usuario especificado")

            # 3) Asegurar que 'stack' sea una lista
            if not isinstance(doc.get("stack"), list):
                await self.collection.update_one(
                    filtro,
                    {"$set": {"stack": []}}
                )

            # 4) Hacer el $push de la nueva skill
            result = await self.collection.update_one(
                filtro,
                {"$push": {"stack": skill}}
            )
            if result.modified_count == 0:
                raise DatabaseException("Error al agregar la habilidad al proyecto")
            return {"message": "Habilidad agregada exitosamente"}
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Excepción al agregar habilidad: {str(e)}") from e

    async def remove_skill(self, skill: str, id: Union[str, int], username: str) -> dict:
        """
        Remueve una habilidad del campo 'stack' del proyecto identificado por `id` y `username`.
        Si la habilidad no existe, lanza NotFoundException.
        Acepta tanto `id` int (legacy) como str con ObjectId (nuevo).
        """
        try:
            # 1) Determinar el filtro según el tipo de id
            if isinstance(id, int) or (isinstance(id, str) and id.isdigit()):
                filtro = {"_id": int(id), "username": username}
            else:
                filtro = {"_id": ObjectId(id), "username": username}

            # 2) Verificar que la skill exista en el proyecto
            exists = await self.collection.find_one({**filtro, "stack": skill})
            if not exists:
                raise NotFoundException("La habilidad no existe en el stack del proyecto")

            # 3) Hacer el $pull para remover la skill
            result = await self.collection.update_one(
                filtro,
                {"$pull": {"stack": skill}}
            )
            if result.modified_count == 0:
                raise DatabaseException("Error al remover la habilidad del proyecto")
            return {"message": "Habilidad removida exitosamente"}
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Excepción al remover habilidad: {str(e)}") from e
