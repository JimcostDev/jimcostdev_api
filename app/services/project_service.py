from datetime import datetime, timezone
from core.database import mongodb
from repositories.project_repository import ProjectRepository
from models.project_model import (
    ProjectCreate,
    ProjectResponse
)
from exceptions import (
    NotFoundException,
    ConflictException,
    DatabaseException
)

class ProjectService:
    def __init__(self):
        self.repo = None

    async def _init_repo(self):
        if not self.repo:
            coll = await mongodb.get_collection("projects")
            self.repo = ProjectRepository(coll)
    
    async def list_projects(self, username: str) -> list[ProjectResponse]:
        await self._init_repo()
        try:
            existing = await self.repo.collection.find_one({"username": username})
            if not existing:
                raise NotFoundException(f"No se encontraron datos para el usuario {username}")
            docs = await self.repo.find_by_username(username)
            return [ProjectResponse(**{**d, "id": d.pop("_id")}) for d in docs]
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error listing project: {e}") from e
        
    async def get_project(self, id: str, username: str) -> ProjectResponse:
        await self._init_repo()
        doc = await self.repo.find_by_id(id)
        if not doc or doc.get("username") != username:
            raise NotFoundException("Project not found")
        # convertir un documento MongoDB en un modelo Pydantic que tiene una propiedad id (en lugar de _id).
        return ProjectResponse(**{**doc, "id": doc.pop("_id")})
         
    async def create_project(
        self, payload: ProjectCreate, username: str
    ) -> ProjectResponse:
        await self._init_repo()
        try:
            existing = await self.repo.collection.find_one({"project": payload.title, "username": username})
            if existing:
                raise ConflictException(f"Project '{payload.title}' already exists for user {username}")
            
            now = datetime.now(timezone.utc).isoformat()
            data = payload.model_dump()
            # Convertir HttpUrl a cadena para almacenamiento
            data['link'] = str(data['link'])
            data['image'] = str(data['image'])
            if data.get("stack") is None:
                data["stack"] = []
            data.update({
            "username": username,
            "created_at": now,
            "updated_at": now
            })
            
            created = await self.repo.create(data)
            return ProjectResponse(**{**created, "id": created.pop("_id")})
        except Exception as e:
            raise DatabaseException("Error creating project") from e
        
    async def update_project(
        self, id: str, payload: ProjectCreate, username: str
    ) -> ProjectResponse:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if doc.get("username") != username:
                raise NotFoundException("Project no pertenece al usuario autenticado")
            
            now = datetime.now(timezone.utc).isoformat()
            data = payload.model_dump(exclude_unset=True)
            # Convertir HttpUrl a cadena para almacenamiento
            if "image" in data:
                data["image"] = str(data["image"])
            if "link" in data:
                data["link"] = str(data["link"])
            data.update({
                "updated_at": now
            })
            
            updated = await self.repo.update(id, data)
            return ProjectResponse(**{**updated, "id": updated.pop("_id")})
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error updating project") from e
        
    async def delete_project(self, id: str, username: str) -> None:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if not doc or doc.get("username") != username:
                raise NotFoundException("Project no pertenece al usuario autenticado o no existe")
            
            await self.repo.delete(id)
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("Error deleting project") from e
        
    # ----------------------------
    # Métodos para agregar y remover skills en el stack
    # ----------------------------
    async def add_skill(self, skill: str, id: str, username: str) -> dict:
        """
        Agrega una habilidad al stack del proyecto indicado.
        'id' puede ser string (ObjectId) o int (legacy).
        """
        await self._init_repo()
        try:
            result = await self.repo.add_skill(skill, id, username)
            return result
        except NotFoundException:
            raise
        except DatabaseException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error agregando habilidad: {str(e)}") from e

    async def remove_skill(self, skill: str, id: str, username: str) -> dict:
        """
        Remueve una habilidad del stack del proyecto indicado.
        'id' puede ser string (ObjectId) o int (legacy).
        """
        await self._init_repo()
        try:
            result = await self.repo.remove_skill(skill, id, username)
            return result
        except NotFoundException:
            raise
        except DatabaseException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error removiendo habilidad: {str(e)}") from e