from typing import List
from fastapi import Depends, HTTPException, APIRouter

from dependencies import SessionDep, admin_required
from repository import UserRepo
from schemas import UserCreate, UserResponse, UserUpdate


router = APIRouter(prefix="/admins", tags=["Admin"])


@router.get("/users/", response_model=List[UserResponse])
async def get_user_list(
    db: SessionDep, 
    is_admin: bool = Depends(admin_required)
):
    """Получение списка пользователей"""
    return await UserRepo.get_all_users(db, UserResponse)


@router.post("/users/create")
async def user_create(
    db: SessionDep, 
    user: UserCreate, 
    is_admin: bool = Depends(admin_required)
):
    """Создание пользователя"""
    new_user = await UserRepo.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")
    return {
        "message": 'Пользователь успешно создан',
        'user': UserResponse.model_validate(new_user)
    }


@router.patch("/users/update/{user_id}")
async def user_update(
    db: SessionDep, 
    user: UserUpdate, 
    user_id: int, 
    is_admin: bool = Depends(admin_required)
):
    """Обновление пользователя"""
    update_user = await UserRepo.update_user(db, user, user_id)
    if not update_user:
        raise HTTPException(status_code=400, detail="Не получилось обновить пользователя")
    return {
        "message": 'Пользователь успешно обновлен',
        'user': UserResponse.model_validate(update_user)
    }


@router.delete("/users/delete/{user_id}")
async def user_delete(
    db: SessionDep, 
    user_id: int, 
    is_admin: bool = Depends(admin_required)
):
    """Удаление пользователя"""
    delete_user = await UserRepo.delete_user(db, user_id)
    if not delete_user:
        raise HTTPException(status_code=400, detail="Не получилось удалить пользователя")
    return {"message": 'Пользователь успешно удален'}
