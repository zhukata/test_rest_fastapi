# test_rest_fastapi


test_rest_fastapi — это RESTful API для управления пользователями включая регистрацию, получение информации о пользователяхб их счетах и платежах. Присутствует эмуляция вебхука, для обработки платежа.


## Требования
* Python 3.12
* Fastapi 0.115.8
* PostgreSQL
* Docker and Docker Compose (для запуска через Docker Compose)

## Эндпоинты
### Эндпоинты для пользователя
1. **POST users/login**: Авторизация пользователя.
2. **GET /users/{user_id}**: Получить информацию о себе по айди.
3. **GET /users/{user_id}/accounts**: Получить список своих счетов.
4. **GET /users/{user_id}/accounts/new**: Создать новый счет.
5. **GET /users/{user_id}/payments**: Получить список своих платежей.

### Эндпоинты для админа
1. **POST /admin/users/**: Получение списка пользователей.
2. **GET /admin/users/{user_id}/accounts**: Получение списка счетов пользователя.
3. **POST /admin/users/create**: Создание пользователя.
4. **PATCH /admin/users/{user_id}**: Обновление пользователя.
5. **DELETE /admin/users/{user_id}**: Удаление пользователя.

. **POST payments/webhook**: Обработка платежа.

## Примеры запросов
### POST admin/users/create
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

### GET admin/users
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

### PATCH admin/users/{user_id}
```json
{
  "email": "user@example.com",
  "full_name": "zhukata_2"
}
```

### POST /payments/webhook
```json
{
  "account_id": 0,
  "amount": 0,
  "transaction_id": "string",
  "user_id": 0,
  "signature": "string"
}
```