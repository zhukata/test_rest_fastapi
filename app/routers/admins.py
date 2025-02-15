from typing import List
from fastapi import Depends, HTTPException, APIRouter

from app.dependencies import SessionDep, admin_required
from app.repository import AccountRepo, UserRepo
from app.schemas import AccountResponse, UserCreate, UserResponse, UserUpdate


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users/", response_model=List[UserResponse])
async def get_users(
    db: SessionDep,
    is_admin: bool = Depends(admin_required)
):
    """Получение списка пользователей"""
    return await UserRepo.get_all_users(db, UserResponse)


@router.get("/users/{user_id}/accounts", response_model=List[AccountResponse])
async def get_user_accounts(
    db: SessionDep,
    user_id: int,
    is_admin: bool = Depends(admin_required)
):
    """Получение списка счетов пользователя"""
    accounts = await AccountRepo.get_accounts(db, user_id, AccountResponse)
    if not accounts:
        raise HTTPException(status_code=404, detail="Счета не найдены")
    return accounts


@router.post("/users/create", response_model=UserResponse)
async def user_create(
    db: SessionDep,
    user: UserCreate,
    is_admin: bool = Depends(admin_required)
):
    """Создание пользователя"""
    new_user = await UserRepo.create_user(db, user)
    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь уже зарегистрирован"
        )
    return UserResponse.model_validate(new_user)


@router.patch("/users/{user_id}", response_model=UserResponse)
async def user_update(
    db: SessionDep,
    user: UserUpdate,
    user_id: int,
    is_admin: bool = Depends(admin_required)
):
    """Обновление пользователя"""
    update_user = await UserRepo.update_user(db, user, user_id)
    if not update_user:
        raise HTTPException(
            status_code=400,
            detail="Не получилось обновить пользователя"
        )
    return UserResponse.model_validate(update_user)


@router.delete("/users/{user_id}", response_model=dict)
async def user_delete(
    db: SessionDep,
    user_id: int,
    is_admin: bool = Depends(admin_required)
):
    """Удаление пользователя"""
    delete_user = await UserRepo.delete_user(db, user_id)
    if not delete_user:
        raise HTTPException(
            status_code=400,
            detail="Не получилось удалить пользователя"
        )
    return {"message": 'Пользователь успешно удален'}
