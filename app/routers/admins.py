from typing import List
from fastapi import HTTPException, Request, Response, APIRouter

from db import SessionDep
from repository import UserRepo, check_admin
from schemas import UserCreate, UserResponse, UserUpdate


router = APIRouter(prefix="/admins", tags=["Admin"])


@router.get("/users/", response_model=List[UserResponse])
async def get_user_list(db: SessionDep, request: Request):
    user_id = request.cookies.get("user_id")
        # check_user = await UserRepo.authenticate_user(db, user)
    if not user_id:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    if not await check_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    users = await UserRepo.get_all_users(db, UserResponse)
    return users


@router.post("/users/create/")
async def user_create(db: SessionDep, user: UserCreate):
    """Создание пользователя"""
    new_user = await UserRepo.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")
    return {
        "message": 'Пользователь успешно создан',
        'user': UserResponse.model_validate(new_user)
        }


@router.patch("/users/update/{user_id}")
async def user_update(db: SessionDep, user: UserUpdate, user_id):
    update_user = await UserRepo.update_user(db, user, int(user_id))
    if not update_user:
        raise HTTPException(status_code=400, detail="Не получилось обновить пользователя")
    return {
        "message": 'Пользователь успешно обновлен',
        'user': UserResponse.model_validate(update_user)
        }


@router.delete("/users/delete/{user_id}")
async def user_delete(db: SessionDep, user_id):
    delete_user = await UserRepo.delete_user(db, int(user_id))
    if not delete_user:
        raise HTTPException(status_code=400, detail="Не получилось удалить пользователя")
    return {"message": 'Пользователь успешно удален'}
