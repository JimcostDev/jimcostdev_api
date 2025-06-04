from datetime import datetime, timezone
from core.database import mongodb
from repositories.profile_repository import ProfileRepository
from models.profile_model import (
    ProfileCreate,
    ProfileResponse
)
from exceptions import (
    NotFoundException,
    ConflictException,
    DatabaseException
)

class ProfileService:
    def __init__(self):
        self.repo = None

    async def _init_repo(self):
        if not self.repo:
            coll = await mongodb.get_collection("perfil")
            self.repo = ProfileRepository(coll)
    
    async def list_profiles(self, username: str) -> list[ProfileResponse]:
        await self._init_repo()
        try:
            existing = await self.repo.collection.find_one({"username": username})
            if not existing:
                raise NotFoundException(f"No se encontraron datos para el usuario {username}")
            docs = await self.repo.find_by_username(username)
            return [ProfileResponse(**{**d, "id": d.pop("_id")}) for d in docs]
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error listing profile: {e}") from e
         
    async def create_profile(
        self, payload: ProfileCreate, username: str
    ) -> ProfileResponse:
        await self._init_repo()
        try:
            existing = await self.repo.collection.find_one({"profile": payload.rol, "username": username})
            if existing:
                raise ConflictException(f"Profile '{payload.rol}' already exists for user {username}")
            
            now = datetime.now(timezone.utc).isoformat()
            data = payload.model_dump()
            # Convertir HttpUrl a cadena para almacenamiento
            data['avatar'] = str(data['avatar'])
            if data.get("skills") is None:
                data["skills"] = []
            data.update({
            "username": username,
            "created_at": now,
            "updated_at": now
            })
            
            created = await self.repo.create(data)
            return ProfileResponse(**{**created, "id": created.pop("_id")})
        except Exception as e:
            raise DatabaseException("Error creating profile") from e
        
    async def update_profile(
        self, id: str, payload: ProfileCreate, username: str
    ) -> ProfileResponse:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if doc.get("username") != username:
                raise NotFoundException("Profile no pertenece al usuario autenticado")
            
            now = datetime.now(timezone.utc).isoformat()
            data = payload.model_dump(exclude_unset=True)
            # Convertir HttpUrl a cadena para almacenamiento
            if "avatar" in data:
                data['avatar'] = str(data['avatar'])
            data.update({
                "updated_at": now
            })
            
            updated = await self.repo.update(id, data)
            return ProfileResponse(**{**updated, "id": updated.pop("_id")})
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error updating profile") from e
        
    async def delete_profile(self, id: str, username: str) -> None:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if not doc or doc.get("username") != username:
                raise NotFoundException("Profile no pertenece al usuario autenticado o no existe")
            
            await self.repo.delete(id)
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error deleting profile") from e
        
    # ----------------------------
    # Skills: add_skill y remove_skill
    # ----------------------------
    async def add_skill(self, skill: str, username: str) -> dict:
        await self._init_repo()
        try:
            result = await self.repo.add_skill(skill, username)
            return result
        except NotFoundException:
            # Si no existe ningún documento con ese username
            raise NotFoundException(f"No se encontró ningún perfil para el usuario '{username}'")
        except Exception as e:
            raise DatabaseException(f"Error agregando habilidad: {str(e)}") from e

    async def remove_skill(self, skill: str, username: str) -> dict:
        await self._init_repo()
        try:
            result = await self.repo.remove_skill(skill, username)
            return result
        except NotFoundException:
            # Si la habilidad no existe en el perfil o no hay perfil
            raise
        except Exception as e:
            raise DatabaseException(f"Error removiendo habilidad: {str(e)}") from e