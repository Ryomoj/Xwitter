from fastapi import FastAPI
import uvicorn

from src.api.timelines import router as timeline_router

app = FastAPI(title="Timeline Service")

app.include_router(timeline_router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)