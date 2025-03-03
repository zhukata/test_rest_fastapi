import pytest_asyncio
import pytest
from pydantic import ValidationError
from httpx import AsyncClient
from app.repository import UserRepo
from app.schemas import UserResponse


@pytest.mark.asyncio
class TestUserCRUD:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, client: AsyncClient, session):
        """Автоматическая фикстура для установки клиента"""
        self.client = client
        self.db = session

    async def test_create_user(self):
        """Тест создания пользователя"""
        new_user = {
            "email": "test@example.com",
            "password": "securepassword",
            "full_name": "Test User"
        }

        response = await self.client.post(
            "admin/users/create",
            json=new_user,
            cookies={'user_id_from_cookie': '2'}
        )

        assert response.status_code == 200
        data = response.json()

        try:
            UserResponse.model_validate(data)
        except ValidationError as e:
            pytest.fail(f"Ошибка валидации данных: {e}")

    async def test_get_users(self):
        """Тест получения списка пользователей"""
        response = await self.client.get(
            "admin/users/",
            cookies={'user_id_from_cookie': '2'}
        )
        assert response.status_code == 200

        data = response.json()
        print(data)
        assert isinstance(data, list)
        assert len(data) == 3

        for user_data in data:
            try:
                UserResponse.model_validate(user_data)
            except ValidationError as e:
                pytest.fail(f"Ошибка валидации данных: {e}")

    async def test_get_user_accounts(self):
        """Тест получения счетов пользователя"""
        response = await self.client.get(
            "admin/users/1/accounts",
            cookies={'user_id_from_cookie': '2'}
        )
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    async def test_update_user(self):
        """Тест обновления пользователя"""
        update_data = {
            "full_name": "Updated Name"
        }

        response = await self.client.patch(
            "admin/users/1",
            json=update_data,
            cookies={'user_id_from_cookie': '2'}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["full_name"] == "Updated Name"

    async def test_delete_user(self):
        """Тест удаления пользователя"""
        response = await self.client.delete(
            "admin/users/1",
            cookies={'user_id_from_cookie': '2'}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Пользователь успешно удален"}
        user = await UserRepo.get_user_by_id(self.db, 1)
        assert user is None