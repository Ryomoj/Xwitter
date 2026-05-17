from fastapi import FastAPI
import uvicorn

from src.api.tweets import router as tweets_router

app = FastAPI(title="Tweet Service")

app.include_router(tweets_router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)