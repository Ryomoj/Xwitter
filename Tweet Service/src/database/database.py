from bson import ObjectId
from bson.errors import InvalidId
from pymongo import AsyncMongoClient


class MongoDBManager:
    async def __aenter__(self):
        self.client = AsyncMongoClient("mongodb://localhost:27017/")
        self.db = self.client["Xwitter"]
        self.collection = self.db["Tweets"]
        return self

    async def read(self, tweet_id: str):
        try:
            obj_id = ObjectId(tweet_id)
            tweet = await self.collection.find_one({"_id": obj_id})
            if tweet and "_id" in tweet:
                tweet["_id"] = str(tweet["_id"])
            return tweet

        except InvalidId:
            return "Передан некорректный id твита"

    async def write(self, tweet):
        result = await self.collection.insert_one(tweet.dict() if hasattr(tweet, 'dict') else tweet)
        return result.inserted_id

    async def update(self, tweet_id, new_tweet):
        _new_tweet = new_tweet.model_dump()
        _new_tweet.pop("_id", None)

        try:
            obj_id = ObjectId(tweet_id)
            await self.collection.update_one(
                {"_id": obj_id},
                {"$set": _new_tweet}
            )
            return obj_id

        except InvalidId:
            return "Передан некорректный id твита"

    async def delete(self, tweet_id):
        try:
            obj_id = ObjectId(tweet_id)
            result = await self.collection.delete_one({"_id": obj_id})
            return f"Удалено: {result.deleted_count}"

        except InvalidId:
            return "Передан некорректный id твита"

    async def __aexit__(self, *args):
        await self.client.close()
