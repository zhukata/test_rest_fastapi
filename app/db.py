import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.auth import hash_password
from app.models import UserORM, AccountORM



load_dotenv()

DATABASE_URL = os.getenv('DB_URL')

engine = create_async_engine(DATABASE_URL, echo=True)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def initialize_database():
    existing_user = await SessionDep.execute(select(UserORM).where(UserORM.email == "test_user@example.com"))
    if existing_user.scalar() is None:
        test_user = UserORM(
            email="test_user@example.com",
            password=hash_password("password"),
            full_name="Test User",
            is_admin=False
        )
        SessionDep.add(test_user)
        await SessionDep.flush()
        test_account = AccountORM(user_id=test_user.id, balance=100.0)
        SessionDep.add(test_account)
    
    existing_admin = await SessionDep.execute(select(UserORM).where(UserORM.email == "admin@example.com"))
    if existing_admin.scalar() is None:
        admin_user = UserORM(
            email="admin@example.com",
            password=hash_password("adminpassword"),
            full_name="Admin User",
            is_admin=True
        )
        SessionDep.add(admin_user)
    
    await SessionDep.commit()