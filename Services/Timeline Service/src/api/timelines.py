from fastapi import APIRouter, Depends

from src.database.redis_client import get_redis_client
from src.database.mongodb_client import MongoDBReader


router = APIRouter(prefix="/timeline", tags=["Сервис Ленты"])


@router.get("/global", summary="Глобальная лента")
async def get_global_timeline(
        limit: int = 20,
        offset: int = 0,
        redis_client=Depends(get_redis_client),
        mongo_reader=Depends(MongoDBReader)
):
    cache_key = f"global_timeline"

    # Есть кэш
    # cached_ids = await redis_client.lrange(cache_key, offset, offset + limit - 1)
    #
    # if cached_ids and offset == 0:
    #     tweets_ids = [tid.decode() if isinstance(tid, bytes) else tid for tid in cached_ids]
    #     tweets = await mongo_reader.get_tweets_by_ids(tweets_ids)
    #     return {"tweets": tweets, "source": "redis", "count": len(tweets)}

    # Нет кэша
    tweets = await mongo_reader.get_raw_tweets(limit, offset)

    if offset == 0 and tweets:
        tweet_ids = [str(tweet["_id"]) for tweet in tweets]
        await redis_client.rpush(cache_key, *tweet_ids)
        await redis_client.ltrim(cache_key, 0, 999)

    return {"tweets": tweets, "source": "mongodb", "count": len(tweets)}


# @router.get("/following", summary="Лента подписок")
# async def get_following_timeline(
#         user_id: int,
#         limit: int = 20,
#         offset: int = 0,
#         redis_client=Depends(get_redis_client),
#         mongo_reader=Depends(reader)
# ):
#     cache_key = f"following_timeline:{user_id}"
#
#     # Есть кэш
#     if offset == 0:
#         cached_ids = await redis_client.lrange(cache_key, 0, limit - 1)
#         if cached_ids:
#             tweets_ids = [tid.decode() if isinstance(tid, bytes) else tid for tid in cached_ids]
#             tweets = await mongo_reader.get_tweets_by_ids(tweets_ids)
#             return {"tweets": tweets, "source": "redis", "count": len(tweets)}
#
#     # Получаем ID пользователей, на кого подписан
#     following_ids = await get_following(user_id)  # Нужно реализовать
#
#     if not following_ids:
#         return {"tweets": [], "message": "У вас нет подписок", "count": 0}
#
#     tweets = await mongo_reader.get_tweets_by_user_ids(
#         following_ids,
#         limit=limit,
#         offset=offset
#     )
#
#     if offset == 0 and tweets:
#         tweet_ids = [str(tweet["_id"]) for tweet in tweets]
#         await redis_client.rpush(cache_key, *tweet_ids)
#         await redis_client.ltrim(cache_key, 0, 999)
#
#     return {"tweets": tweets, "source": "mongodb", "count": len(tweets)}