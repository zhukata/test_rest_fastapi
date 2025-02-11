from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from init_db import initialize_database
from db import engine
from models import Base
from routers.users import router as users_router
from routers.admins import router as admins_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await initialize_database()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(admins_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)