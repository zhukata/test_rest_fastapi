from typing import List
from fastapi import HTTPException, Request, Response, APIRouter

from db import SessionDep
from schemas import UserCreate, UserLogin, UserResponse
from repository import authenticate_user, check_admin, create_user, get_user_by_id, get_users


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_user_list(db: SessionDep, request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    if not check_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    users = await get_users(db, UserResponse)
    return users


@router.post("/register")
async def register(db: SessionDep, user: UserCreate):
    new_user = await create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="User уже зарегистрирован")
    return {"message": 'User успешно создан', 'user': new_user}

@router.post("/login")
async def login(db: SessionDep, user: UserLogin, response: Response):
    """Авторизация через email/password"""
    check_user = await authenticate_user(db,user)
    if check_user is None:
        raise HTTPException(status_code=401,
                            detail='Неверная почта или пароль')

    response.set_cookie(key="user_id", value=str(check_user.id), httponly=True)
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

