from datetime import datetime, timezone
from pydantic import EmailStr
from models.user_model import (
    UserModel,
    UserUpdateModel,
    ResetPasswordModel,
    UserResponseModel,
)
from core.database import mongodb
from repositories.user_repository import UserRepository
from utils.hash_and_verify_password import hash_password
from exceptions import (
    NotFoundException,
    ConflictException,
    UnauthorizedException,
    ValidationException,
    DatabaseException,
)

class UserService:
    def __init__(self):
        self.repo = None
    
    async def _init_repo(self):
        """Inicializa el repositorio de usuarios de forma asíncrona"""
        if self.repo is None:
            users_collection = await mongodb.get_collection("users")
            self.repo = UserRepository(users_collection)

    async def create_user(self, new_user: UserModel) -> UserResponseModel:
        await self._init_repo()
        try:
            if await self.repo.find_by_email(new_user.email):
                raise ConflictException("Email ya en uso")
            if await self.repo.find_by_username(new_user.username):
                raise ConflictException("Username ya en uso")

            now = datetime.now(timezone.utc).isoformat()
            user_data = new_user.model_dump(exclude={"confirm_password"})
            
            user_data.update({
                "password": await hash_password(new_user.password),
                "created_at": now,
                "updated_at": now,
                "roles": ["admin"],
            })

            created = await self.repo.create_user(user_data)
            return UserResponseModel(**{**created, "id": created.pop("_id")})
        
        except ValidationException:
            raise
        except Exception as ex:
            raise DatabaseException(str(ex))

    async def get_user(self, username: str) -> UserResponseModel:
        await self._init_repo()
        try:
            found = await self.repo.find_by_username(username)
            if not found:
                raise NotFoundException("Usuario no encontrado")
            return UserResponseModel(**{**found, "id": found.pop("_id")})
        except NotFoundException:
            raise
        except Exception as ex:
            raise DatabaseException(str(ex))
        
    async def get_user_by_email(self, email: EmailStr) -> UserResponseModel:
        await self._init_repo()
        try:
            found = await self.repo.find_by_email(email)
            if not found:
                raise NotFoundException("Usuario no encontrado")
            return UserResponseModel(**{**found, "id": found.pop("_id")})
        except NotFoundException:
            raise
        except Exception as ex:
            raise DatabaseException(str(ex))

    # Nuevo método para actualizar usuario autenticado
    async def update_authenticated_user(
        self, 
        current_username: str, 
        payload: UserUpdateModel
    ) -> UserResponseModel:
        await self._init_repo()
        try:
            # Verificar que el usuario existe
            existing = await self.repo.find_by_username(current_username)
            if not existing:
                raise NotFoundException("Usuario no existe")

            # Verificar nuevo email si es diferente
            if payload.email and payload.email != existing["email"]:
                if await self.repo.find_by_email(payload.email):
                    raise ConflictException("Email en uso")

            data = payload.model_dump(
                exclude_unset=True, 
                exclude={"confirm_password"}
            )
            
            # Hashear nueva contraseña si se proporciona
            if data.get("password"):
                data["password"] = await hash_password(data["password"])
            
            data["updated_at"] = datetime.now(timezone.utc).isoformat()

            updated = await self.repo.update_user(existing["_id"], data)
            return UserResponseModel(**{**updated, "id": updated.pop("_id")})
        
        except (NotFoundException, ConflictException):
            raise
        except Exception as ex:
            raise DatabaseException(str(ex))

    # Nuevo método para eliminar usuario autenticado
    async def delete_authenticated_user(self, username: str) -> None:
        await self._init_repo()
        try:
            existing = await self.repo.find_by_username(username)
            if not existing:
                raise NotFoundException("Usuario no existe")
            await self.repo.delete_user(existing["_id"])
        except NotFoundException:
            raise
        except Exception as ex:
            raise DatabaseException(str(ex))


    async def update_user(self, username: str, payload: UserUpdateModel) -> UserResponseModel:
        await self._init_repo()
        try:
            existing = await self.repo.find_by_username(username)
            if not existing:
                raise NotFoundException("Usuario no existe")

            # Verificar nuevo email si es diferente
            if payload.email and payload.email != existing["email"]:
                if await self.repo.find_by_email(payload.email):
                    raise ConflictException("Email en uso")

            data = payload.model_dump(
                exclude_unset=True, 
                exclude={"confirm_password"}
            )
            
            # Hashear nueva contraseña si se proporciona
            if data.get("password"):
                data["password"] = await hash_password(data["password"])
            
            data["updated_at"] = datetime.now(timezone.utc).isoformat()

            updated = await self.repo.update_user(existing["_id"], data)
            return UserResponseModel(**{**updated, "id": updated.pop("_id")})
        
        except (NotFoundException, ConflictException):
            raise
        except Exception as ex:
            raise DatabaseException(str(ex))

    async def reset_password(
        self, 
        username: str, 
        secret: str, 
        payload: ResetPasswordModel
    ) -> UserResponseModel:
        await self._init_repo()
        try:
            existing = await self.repo.find_by_username(username)
            if not existing:
                raise NotFoundException("Usuario no existe")
            
            # Validar secreto de recuperación
            if secret != existing.get("secret"):
                raise UnauthorizedException("Secreto inválido")

            data = payload.model_dump(
                exclude_unset=True, 
                exclude={"confirm_password"}
            )
            
            if data.get("password"):
                data["password"] = await hash_password(data["password"])
            
            data["updated_at"] = datetime.now(timezone.utc).isoformat()

            updated = await self.repo.update_user(existing["_id"], data)
            return UserResponseModel(**{**updated, "id": updated.pop("_id")})
        
        except (NotFoundException, UnauthorizedException):
            raise
        except Exception as ex:
            raise DatabaseException(str(ex))

    async def delete_user(self, username: str) -> None:
        await self._init_repo()
        try:
            existing = await self.repo.find_by_username(username)
            if not existing:
                raise NotFoundException("Usuario no existe")
            await self.repo.delete_user(existing["_id"])
        except NotFoundException:
            raise
        except Exception as ex:
            raise DatabaseException(str(ex))