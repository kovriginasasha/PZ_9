from typing import Any, List, Optional

from beanie import PydanticObjectId, init_beanie
from pymongo import AsyncMongoClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from models.events import Event
from models.trainings import Training
from models.users import User


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")

    async def initialize_database(self):
        client = AsyncMongoClient(self.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[Event, User, Training],
        )


class Database:
    def __init__(self, model):
        self.model = model

    # CREATE
    async def save(self, document) -> None:
        await document.create()

    # READ
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        return await self.model.find_all().to_list()

    # UPDATE
    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc = await self.get(id)
        if not doc:
            return False
        fields = body.model_dump(exclude_none=True)
        await doc.update({"$set": fields})
        return await self.get(id)

    # DELETE
    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
