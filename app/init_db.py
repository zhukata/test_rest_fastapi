from sqlalchemy import select

from db import new_session
from auth import hash_password
from models import UserORM, AccountORM


async def initialize_database():
    """Создание тестовых сущностей"""
    async with new_session() as session:
        existing_user = await session.execute(
            select(UserORM).where(UserORM.email == "test_user@example.com")
        )
        if existing_user.scalar() is None:
            test_user = UserORM(
                email="test_user@example.com",
                password=hash_password("password"),
                full_name="Test User",
                is_admin=False
            )
            session.add(test_user)
            await session.flush()

            test_account = AccountORM(user_id=test_user.id, balance=100.0)
            session.add(test_account)

        existing_admin = await session.execute(
            select(UserORM).where(UserORM.email == "admin@example.com")
        )
        if existing_admin.scalar() is None:
            admin_user = UserORM(
                email="admin@example.com",
                password=hash_password("adminpassword"),
                full_name="Admin User",
                is_admin=True
            )
            session.add(admin_user)

        await session.commit()
