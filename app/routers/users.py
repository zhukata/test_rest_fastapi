from typing import List
from fastapi import HTTPException, Request, Response, APIRouter

from db import SessionDep
from schemas import UserCreate, UserLogin, UserResponse
from repository import authenticate_user, check_admin, create_user, get_user_by_id, get_users


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login")
async def login(db: SessionDep, user: UserLogin, response: Response):
    """Авторизация через email/password"""
    check_user = await authenticate_user(db,user)
    if check_user is None:
        raise HTTPException(status_code=401,
                            detail='Неверная почта или пароль')

    response.set_cookie(key="user_id", value=str(check_user.id), expires=120, httponly=True)
    return {"message": "Успешный вход"}




@router.get("/me", response_model=UserResponse)
async def get_user(request: Request, db: SessionDep):
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не авторизован")

    db_user = await get_user_by_id(db, UserResponse, int(user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return db_user

