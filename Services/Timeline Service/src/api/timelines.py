from typing import Annotated

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/timelines", tags=["Сервис Ленты"])


@router.get("/{}", summary="")
async def get_timeline():
    pass
