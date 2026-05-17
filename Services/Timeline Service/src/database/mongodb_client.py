from pymongo import AsyncMongoClient
from typing import List, Dict, Any
from bson import ObjectId


class MongoDBReader:
    def __init__(self):
        self.client = AsyncMongoClient("mongodb://localhost:27017/")
        self.db = self.client["Xwitter"]
        self.collection = self.db["Tweets"]

    async def get_tweets_by_ids(self, tweet_ids: List[str]) -> List[Dict[str, Any]]:
        """Получает твиты по их ID (батч-запрос)"""
        if not tweet_ids:
            return []

        object_ids = []
        for id in tweet_ids:
            try:
                object_ids.append(ObjectId(id))
            except:
                pass

        cursor = self.collection.find({"_id": {"$in": object_ids}})
        tweets = await cursor.to_list(length=20)

        for tweet in tweets:
            tweet["_id"] = str(tweet["_id"])

        tweets_dict = {tweet["_id"]: tweet for tweet in tweets}
        sorted_tweets = [tweets_dict[id] for id in tweet_ids if id in tweets_dict]

        return sorted_tweets

    async def get_raw_tweets(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        cursor = self.collection.find().sort("created_at", -1).skip(offset).limit(limit)
        tweets = await cursor.to_list(length=limit)

        for tweet in tweets:
            tweet["_id"] = str(tweet["_id"])

        return tweets

    # async def get_tweets_by_user_ids(
    #         self,
    #         user_ids: List[int],
    #         limit: int = 20,
    #         offset: int = 0
    # ) -> List[Dict]:
    #     """Получить твиты от конкретных пользователей"""
    #     cursor = self.tweets_collection.find(
    #         {"user_id": {"$in": user_ids}}
    #     ).sort("created_at", -1).skip(offset).limit(limit)
    #
    #     tweets = await cursor.to_list(length=limit)
    #
    #     for tweet in tweets:
    #         tweet["_id"] = str(tweet["_id"])
    #
    #     return tweets