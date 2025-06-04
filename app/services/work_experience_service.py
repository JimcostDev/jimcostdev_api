from datetime import datetime
from core.database import mongodb
from repositories.work_experience_repository import WorkExperienceRepository
from models.work_experience_model import (
    WorkExperienceCreate,
    WorkExperienceResponse
)
from exceptions import (
    NotFoundException,
    DatabaseException
)
from typing import List, Union


class WorkExperienceService:
    def __init__(self):
        self.repo: WorkExperienceRepository | None = None

    async def _init_repo(self):
        if not self.repo:
            coll = await mongodb.get_collection("work_experience")
            self.repo = WorkExperienceRepository(coll)

    # ----------------------------
    # Funciones de cálculo de duración
    # ----------------------------
    @staticmethod
    def calculate_duration(initial_date: str, end_date: str | None) -> str:
        """
        Calcula la duración entre initial_date y end_date en formato:
        - "X años y Y meses"  
        - "X años" si meses = 0  
        - "Y meses" si años = 0  
        Si end_date es None, usa la fecha actual.
        """
        # Parsear fechas
        initial_dt = datetime.fromisoformat(initial_date)
        end_dt = datetime.now() if end_date is None else datetime.fromisoformat(end_date)
        diff = end_dt - initial_dt

        total_days = diff.days
        years = total_days // 365
        months = (total_days % 365) // 30

        if years == 0:
            return f"{months} meses" if months != 0 else "0 meses"
        if months == 0:
            return f"{years} años"
        años_str = f"{years} año{'s' if years > 1 else ''}"
        meses_str = f"{months} mes{'es' if months > 1 else ''}"
        return f"{años_str} y {meses_str}"

    @staticmethod
    def calculate_duration_years(initial_date: str, end_date: str | None) -> float:
        """
        Calcula la duración en años (float) entre initial_date y end_date.
        Si end_date es None, usa la fecha actual.
        """
        initial_dt = datetime.fromisoformat(initial_date)
        end_dt = datetime.now() if end_date is None else datetime.fromisoformat(end_date)
        diff = end_dt - initial_dt
        return diff.days / 365

    # ----------------------------
    # Listar experiencias con duración
    # ----------------------------
    async def list_WorkExperience(self, username: str) -> List[WorkExperienceResponse]:
        await self._init_repo()
        try:
            # Verificar que exista al menos un documento para el usuario
            exists = await self.repo.collection.find_one({"username": username})
            if not exists:
                raise NotFoundException(f"No se encontraron datos para el usuario {username}")

            docs = await self.repo.find_by_username(username)
            respuestas: List[WorkExperienceResponse] = []

            for d in docs:
                raw_id = d.pop("_id")
                duration_str = self.calculate_duration(d["initial_date"], d.get("end_date"))
                payload = {
                    "id": str(raw_id),
                    "rol": d.get("rol", ""),
                    "company": d.get("company", ""),
                    "location": d.get("location", ""),
                    "activities": d.get("activities", ""),
                    "initial_date": d.get("initial_date", ""),
                    "end_date": d.get("end_date"),
                    "username": d.get("username"),
                    "duration": duration_str
                }
                respuestas.append(WorkExperienceResponse(**payload))

            return respuestas

        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error listing WorkExperience: {e}") from e

    # ----------------------------
    # Obtener experiencia por ID con duración
    # ----------------------------
    async def get_WorkExperience(self, id: Union[str, int], username: str) -> WorkExperienceResponse:
        await self._init_repo()
        doc = await self.repo.find_by_id(id)
        if not doc or doc.get("username") != username:
            raise NotFoundException("WorkExperience not found")

        raw_id = doc.pop("_id")
        duration_str = self.calculate_duration(doc["initial_date"], doc.get("end_date"))
        payload = {
            "id": str(raw_id),
            "rol": doc.get("rol", ""),
            "company": doc.get("company", ""),
            "location": doc.get("location", ""),
            "activities": doc.get("activities", ""),
            "initial_date": doc.get("initial_date", ""),
            "end_date": doc.get("end_date"),
            "username": doc.get("username"),
            "duration": duration_str
        }
        return WorkExperienceResponse(**payload)

    # ----------------------------
    # Crear experiencia laboral
    # ----------------------------
    async def create_WorkExperience(
        self, payload: WorkExperienceCreate, username: str
    ) -> WorkExperienceResponse:
        await self._init_repo()
        try:
            # Opcional: puedes chequear duplicados según algún criterio, p.ej. rol + empresa.
            now_iso = datetime.now().isoformat()
            data = payload.model_dump()
            data.update({
                "username": username,
                "created_at": now_iso,
                "updated_at": now_iso
            })

            created = await self.repo.create(data)
            raw_id = created.pop("_id")
            duration_str = self.calculate_duration(created["initial_date"], created.get("end_date"))

            respuesta = {
                "id": str(raw_id),
                "rol": created.get("rol", ""),
                "company": created.get("company", ""),
                "location": created.get("location", ""),
                "activities": created.get("activities", ""),
                "initial_date": created.get("initial_date", ""),
                "end_date": created.get("end_date"),
                "username": created.get("username"),
                "duration": duration_str
            }
            return WorkExperienceResponse(**respuesta)

        except Exception as e:
            raise DatabaseException(f"Error creating WorkExperience: {e}") from e

    # ----------------------------
    # Actualizar experiencia laboral
    # ----------------------------
    async def update_WorkExperience(
        self, id: Union[str, int], payload: WorkExperienceCreate, username: str
    ) -> WorkExperienceResponse:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if not doc or doc.get("username") != username:
                raise NotFoundException("WorkExperience no pertenece al usuario autenticado")

            data = payload.model_dump(exclude_unset=True)
            data["updated_at"] = datetime.now().isoformat()

            updated = await self.repo.update(id, data)
            raw_id = updated.pop("_id")
            duration_str = self.calculate_duration(updated["initial_date"], updated.get("end_date"))

            respuesta = {
                "id": str(raw_id),
                "rol": updated.get("rol", ""),
                "company": updated.get("company", ""),
                "location": updated.get("location", ""),
                "activities": updated.get("activities", ""),
                "initial_date": updated.get("initial_date", ""),
                "end_date": updated.get("end_date"),
                "username": updated.get("username"),
                "duration": duration_str
            }
            return WorkExperienceResponse(**respuesta)

        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error updating WorkExperience: {e}") from e

    # ----------------------------
    # Eliminar experiencia laboral
    # ----------------------------
    async def delete_WorkExperience(self, id: Union[str, int], username: str) -> None:
        await self._init_repo()
        try:
            doc = await self.repo.find_by_id(id)
            if not doc or doc.get("username") != username:
                raise NotFoundException("WorkExperience no pertenece al usuario autenticado o no existe")

            await self.repo.delete(id)
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error deleting WorkExperience: {e}") from e

    # ----------------------------
    # Total de años de experiencia laboral
    # ----------------------------
    async def get_total_work_experience(self, username: str) -> int:
        await self._init_repo()
        try:
            docs = await self.repo.find_by_username(username)
            if not docs:
                return 0

            total_years = 0.0
            for d in docs:
                total_years += self.calculate_duration_years(
                    d["initial_date"], d.get("end_date")
                )
            return round(total_years)
        except Exception as e:
            raise DatabaseException(f"Error calculating total work experience: {e}") from e
