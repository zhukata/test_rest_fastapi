import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession



load_dotenv()

DATABASE_URL = os.getenv('DB_URL')

engine = create_async_engine(DATABASE_URL, echo=True)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


# async def create_tables():
#    async with engine.begin() as conn:
#        await conn.run_sync(Model.metadata.create_all)

# async def delete_tables():
#    async with engine.begin() as conn:
#        await conn.run_sync(Model.metadata.drop_all)
