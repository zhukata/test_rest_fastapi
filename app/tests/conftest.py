import asyncio
import os
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.db import Base, get_session
from app.init_db import initialize_database


load_dotenv()
TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')

engine = create_async_engine(TEST_DATABASE_URL, echo=True)

TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)



@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await initialize_database(TestingSessionLocal)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture()
async def session():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture()
async def client(session: AsyncSession):
    async def override_get_db():
        yield session
    app.dependency_overrides[get_session] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test") as c:
        yield c

@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Глобальный event loop для всех тестов."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# @pytest_asyncio.fixture
# async def test_db():
#     """Создаёт тестовую БД и откатывает изменения после теста"""
#     async with TestingSessionLocal() as session:
#         yield session
#         await session.rollback()


# @pytest_asyncio.fixture(scope="session", autouse=True)
# async def setup_test_db():
#     """Создаёт структуру БД перед тестами"""
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)  # Удаляем все таблицы
#         await conn.run_sync(Base.metadata.create_all)  # Создаём заново

#     await initialize_database(TestingSessionLocal) 


# @pytest_asyncio.fixture
# async def client(test_db: AsyncSession):
#     """Фикстура HTTP-клиента, использующего тестовую БД"""

#     # Подменяем зависимость `get_session`, чтобы использовать тестовую БД
#     async def override_get_session():
#         yield test_db

#     app.dependency_overrides[get_session] = override_get_session

#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test",
#     ) as ac:
#         yield ac

#     app.dependency_overrides.clear()  
