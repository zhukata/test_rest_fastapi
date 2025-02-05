# test_rest_fastapi


test_rest_fastapi — это RESTful API для управления пользователями включая регистрацию и получение информации о пользователях.


## Требования
* Python 3.12
* Fastapi 0.115.8
* PostgreSQL
* Docker and Docker Compose (для запуска через Docker Compose)

## Эндпоинты
1. **POST users/register**: Создать пользователя.
2. **POST users/login**: Авторизация пользователя
3. **GET /users**: Получить список пользователей.
4. **GET /users/{user_id}**: Получить пользователя по айди.

## Примеры запросов
### POST users/register
```json
{
  "email": "user@example.com",
  "full_name": "zhukata",
  "password": "password"
}
```

### POST users/login
```json
{
  "email": "user@example.com",
  "password": "password"
}
```

### GET /users
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "zhukata"
  },
  {
    "id": 2,
    "email": "user2@example.com",
    "full_name": "test2"
  }
]
```

### GET /users/{user_id}
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "zhukata"
}
```