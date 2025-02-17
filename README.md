# test_rest_fastapi


test_rest_fastapi — это RESTful API для управления пользователями включая регистрацию, получение информации о пользователях их счетах и платежах. Присутствует эмуляция вебхука, для обработки платежа.


## Требования
* Python 3.12
* Fastapi 0.115.8
* PostgreSQL
* Docker and Docker Compose (для запуска через Docker Compose)


## Инструкция по запуску проекта

### 1. Запуск с использованием Docker Compose  
Этот способ самый простой, так как автоматически настраивает окружение и зависимости.  

### Шаги:  
1. Убедитесь, что у вас установлены **Docker** и **Docker Compose**.  
2. Клонируйте репозиторий:  
   ```
   git clone https://github.com/zhukata/test_rest_fastapi
   cd test_rest_fastapi
   ```
3. Создайте файл .env и укажите в нем переменные окружения
```
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/db_name
SECRET_KEY = 'your secret key'
POSTGRES_USER = user
POSTGRES_PASSWORD = password
POSTGRES_DB = db_name
```
4. Запустите проект командой:
```
docker-compose up --build
```
5. API будет доступно по адресу: http://localhost:8000

### 2.Запуск без Docker (локально)
1. Убедитесь что у вас установленны Python 3.12+ и PostgreSQL.
2. Установите зависимости:
```
pip install -r requirements.txt
```
3. Укажите переменные окружения в .env (см. выше).
4. Выполните миграции базы данных:
```
alembic upgrade head

```
5. Запустите сервер FastAPI:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
6. API доступно по адресу: http://localhost:8000

### 3. Данные пользователей по умолчанию:
1. admin
```
email(admin@example.com)
password(adminpassword) 
```
2. user
```
email(test_user@example.com)
password(password)
```


## Эндпоинты
### Эндпоинты для пользователя:
1. **POST users/login**: Авторизация пользователя.
2. **GET /users/{user_id}**: Получить информацию о себе по айди.
3. **GET /users/{user_id}/accounts**: Получить список своих счетов.
4. **GET /users/{user_id}/accounts/new**: Создать новый счет.
5. **GET /users/{user_id}/payments**: Получить список своих платежей.

### Эндпоинты для админа:
1. **POST /admin/users/**: Получение списка пользователей.
2. **GET /admin/users/{user_id}/accounts**: Получение списка счетов пользователя.
3. **POST /admin/users/create**: Создание пользователя.
4. **PATCH /admin/users/{user_id}**: Обновление пользователя.
5. **DELETE /admin/users/{user_id}**: Удаление пользователя.

### Эндпоинт транзакции:
**POST payments/webhook**: Обработка платежа.

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