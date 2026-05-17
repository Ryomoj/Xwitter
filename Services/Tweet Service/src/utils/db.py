from typing import Annotated

from fastapi import Depends

from src.database.database import MongoDBManager


async def get_db():
    async with MongoDBManager() as db:
        yield db

DatabaseDep = Annotated[MongoDBManager, Depends(get_db)]