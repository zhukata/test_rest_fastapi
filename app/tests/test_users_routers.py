import pytest_asyncio
import pytest
from pydantic import ValidationError
from httpx import AsyncClient
from app.repository import UserRepo
from app.schemas import AccountResponse, UserResponse


@pytest.mark.asyncio
class TestUsersRouters:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, client: AsyncClient, session):
        """Автоматическая фикстура для установки клиента"""
        self.client = client
        self.db = session

    async def test_login(self):
        """Тест авторизации пользователя"""
        user = {
            "email": "test_user@example.com",
            "password": "password",
        }

        response = await self.client.post(
            "users/login",
            json=user,
        )
        assert response.status_code == 200

        data = response.json()
        assert data == {"message": "Успешный вход"}
        assert response.cookies == {'user_id_from_cookie': '1'}
    
    async def test_get_user(self):
        """Тест получения данных пользователя"""
        user_id = 1
        response = await self.client.get(
            f"users/{user_id}",
            cookies={'user_id_from_cookie': str(user_id)}
        )
        assert response.status_code == 200

        data = response.json()
        assert data == {
            'id': 1,
            'email': 'test_user@example.com',
            'full_name': 'Test User'
        }
        assert UserResponse.model_validate(data)

    async def test_create_account(self):
        """Тест создания счета пользователя"""
        user_id = 1
        response = await self.client.post(
            f"users/{user_id}/accounts/new",
            cookies={'user_id_from_cookie': str(user_id)}
        )
        assert response.status_code == 200

        data = response.json()
        assert data['balance'] == 0.0
        assert AccountResponse.model_validate(data)

    async def test_get_accounts(self):
        """Тест получения счетов пользователя"""
        user_id = 1
        response = await self.client.get(
            f"users/{user_id}/accounts",
            cookies={'user_id_from_cookie': str(user_id)}
        )
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        for account in data:
            try:
                AccountResponse.model_validate(account)
            except ValidationError as e:
                pytest.fail(f"Ошибка валидации данных: {e}")
    
    async def test_get_payments(self):
        """Тест получения платежей пользователя"""
        user_id = 1
        response = await self.client.get(
            f"users/{user_id}/payments",
            cookies={'user_id_from_cookie': str(user_id)}
        )
        assert response.status_code == 404

        data = response.json()
        assert data == {'detail': 'Платежи не найдены'}


@pytest.mark.asyncio
class TestUsersRoutersNegative:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, client: AsyncClient, session):
        """Автоматическая фикстура для установки клиента"""
        self.client = client
        self.db = session
    
    async def test_login_negative(self):
        """Тест ошибок авторизации пользователя"""
        user = {
            "email": "test_user@example.com",
            "password": "",
        }

        response = await self.client.post(
            "users/login",
            json=user,
        )
        assert response.status_code == 401

        data = response.json()
        assert data == {'detail':'Неверная почта или пароль'}

    
    async def test_get_user_no_permission(self):
        """Тест получения данных другого пользователя"""
        user_id = 1
        other_user_id = 2
        response = await self.client.get(
            f"users/{other_user_id}",
            cookies={'user_id_from_cookie': str(user_id)}
        )
        assert response.status_code == 403

        data = response.json()
        assert data == {
            'detail':"Недастаточно прав для просмотра другого пользователя"
        }

    async def test_get_user_negative(self):
        """Тест получения данных несуществуещего пользователя"""
        user_id = 105
        response = await self.client.get(
            f"users/{user_id}",
            cookies={'user_id_from_cookie': str(user_id)}
        )
        assert response.status_code == 404

        data = response.json()
        assert data == {
            'detail':"Пользователь не найден"
        }

    async def test_get_accounts_negative(self):
        """Тест получения счетов пользователя"""
        user_id = 2
        response = await self.client.get(
            f"users/{user_id}/accounts",
            cookies={'user_id_from_cookie': str(user_id)}
        )
        assert response.status_code == 404

        data = response.json()
        assert data == {'detail': 'Счета не найдены'}
    
