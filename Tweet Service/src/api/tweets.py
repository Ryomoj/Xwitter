from fastapi import APIRouter

from src.schemas.tweets import TweetAddSchema, TweetUpdateSchema
from src.utils.db import DatabaseDep

router = APIRouter(prefix="/tweets", tags=["Сервис Твитов"])

@router.get("/{tweet_id}", summary="Получить твит")
async def get_tweet(
        tweet_id: str,
        db: DatabaseDep
):
    result = await db.read(tweet_id)

    return result

@router.post("", summary="Создать твит")
async def create_tweet(
        db: DatabaseDep,
        tweet: TweetAddSchema
):
    result = await db.write(tweet)

    return f"В базу данных добавлен твит: {result}"


@router.patch("/{tweet_id}", summary="Изменить твит")
async def update_tweet(
        tweet_id: str,
        db: DatabaseDep,
        new_tweet: TweetUpdateSchema
):
    result = await db.update(tweet_id, new_tweet)

    return f"В базе данных изменен твит с ID: {result}"


@router.delete("/{tweet_id}", summary="Удалить твит")
async def delete_tweet(
        tweet_id: str,
        db: DatabaseDep
):
    result = await db.delete(tweet_id)

    return result