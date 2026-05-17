from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class TweetAddSchema(BaseModel):
    user_id: int
    created_at: datetime
    text: str = Field(max_length=280)
    media_id: str | None = None
    likes_count: int = 0
    dislikes_count: int = 0


class TweetUpdateSchema(BaseModel):
    text: str | None = None
    media_id: str | None = None
