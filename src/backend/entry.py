from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import globalBackgroundTaskManager, schemaRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    До yield - запуск. После yield - выключение.
    """
    print("Application starting...")
    yield
    await globalBackgroundTaskManager.gatherTasks()
    print("Application shutting down.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schemaRouter)


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}
