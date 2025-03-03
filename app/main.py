from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from app.init_db import initialize_database
from app.db import engine, new_session
from app.models import Base
from app.routers.users import router as users_router
from app.routers.admins import router as admins_router
from app.routers.payments import router as payments_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.create_all)
        # await conn.commit()
        await initialize_database(new_session)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(admins_router)
app.include_router(payments_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

