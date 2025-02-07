from typing import List
from fastapi import HTTPException, Request, Response, APIRouter

from app.auth import check_admin_key
from app.db import SessionDep
from app.repository import check_admin, create_user, get_users
from app.schemas import UserCreate, UserResponse


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=List[UserResponse])
async def get_user_list(db: SessionDep, request: Request):
    user_id = request.cookies.get("user_id")
    print(user_id)
    if not user_id:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    if not await check_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    users = await get_users(db, UserResponse)
    return users


@router.post("users/create")
async def user_create(db: SessionDep, user: UserCreate):
    """Создание пользователя"""
    new_user = await create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="User уже зарегистрирован")
    return {"message": 'User успешно создан', 'user': new_user}


@router.patch("users/update/{user_id}")
async def user_update(db: SessionDep, user: UserCreate):
    update_user = await create_user(db, user)
    if not update_user:
        raise HTTPException(status_code=400, detail="Не получилось обновить пользователя")
    return {"message": 'User успешно обновлен', 'user': update_user}