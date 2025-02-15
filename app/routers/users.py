from typing import List
from fastapi import Depends, HTTPException, Response, APIRouter

from app.dependencies import SessionDep, check_user_permission
from app.schemas import AccountResponse, PaymentResponse, UserLogin, UserResponse
from app.repository import AccountRepo, PaymentRepo, UserRepo


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login")
async def login(db: SessionDep, user: UserLogin, response: Response):
    """Авторизация через email/password"""
    check_user = await UserRepo.authenticate_user(db, user)
    if check_user is None:
        raise HTTPException(status_code=401,
                            detail='Неверная почта или пароль')

    response.set_cookie(
        key="user_id_from_cookie",
        value=str(check_user.id),
        max_age=300,
        httponly=True
    )
    return {"message": "Успешный вход"}


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    db: SessionDep,
    user_id: int,
    is_permission: bool = Depends(check_user_permission)
):
    """Получение данных пользователя"""
    db_user = await UserRepo.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return UserResponse.model_validate(db_user)


@router.get("/{user_id}/accounts", response_model=List[AccountResponse])
async def get_accounts(
    db: SessionDep,
    user_id: int,
    is_permission: bool = Depends(check_user_permission)
):
    """Получение списка счетов пользователя"""
    accounts = await AccountRepo.get_accounts(
        db,
        user_id,
        AccountResponse
    )
    if not accounts:
        raise HTTPException(status_code=404, detail="Счета не найдены")
    return accounts


@router.post("/{user_id}/accounts/new", response_model=AccountResponse)
async def create_account(
    db: SessionDep,
    user_id: int,
    is_permission: bool = Depends(check_user_permission)
):
    """Создание нового счета пользователя"""
    new_account = await AccountRepo.create_account(
        db,
        user_id,
        AccountResponse
    )
    if not new_account:
        raise HTTPException(
            status_code=400,
            detail="Ошибка при создании счета"
        )
    return new_account


@router.get("/{user_id}/payments", response_model=List[PaymentResponse])
async def get_payments(
    db: SessionDep,
    user_id: int,
    is_permission: bool = Depends(check_user_permission)
):
    """Получение списка платежей пользователя"""
    payments = await PaymentRepo.get_payments(
        db,
        user_id,
        PaymentResponse
    )
    if not payments:
        raise HTTPException(status_code=404, detail="Платежи не найдены")
    return payments
