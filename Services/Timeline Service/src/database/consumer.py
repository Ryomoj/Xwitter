from fastapi import Depends

from src.database import redis_client
from src.database.redis_client import get_redis_client


# Слушаем Kafka и добавляем новые твиты в ленты подписчиков
async def on_new_tweet(
        tweet,
        redis_client=Depends(get_redis_client)
):
    tweet_id = str(tweet["_id"])

    # Получаем список подписчиков автора (из Follow Service)
    followers = await get_user_followers(tweet["user_id"])

    # Добавляем твит в ленту каждого подписчика
    for follower_id in followers:
        cache_key = f"timeline:{follower_id}"
        await redis_client.lpush(cache_key, tweet_id)
        await redis_client.ltrim(cache_key, 0, 999)  # Оставляем последние 1000