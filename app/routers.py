from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request, Response, APIRouter

from db import SessionDep
from schemas import UserCreate, UserLogin, UserResponse
from repository import create_user, get_user_by_email, get_users
from auth import verify_password


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_user_list(request: Request, db: SessionDep):
    users = await get_users(db, UserResponse)
    return users


@router.post("/register", response_model=UserCreate)
async def register(user: UserCreate, db: SessionDep):
    new_user = await create_user(db, user)
    return {"message": 'User успешно создан', 'user': new_user}

@router.post("/login")
async def login(user: UserLogin, db: SessionDep, response: Response):
    """Авторизация через email/password"""
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    response.set_cookie(key="user_id", value=str(db_user.id), httponly=True)
    return {"message": "Успешный вход"}

@router.get("/{id}", response_model=UserResponse)
async def get_user(request: Request, db: SessionDep):
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не авторизован")

    db_user = await get_user_by_email(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return {'user': db_user}

