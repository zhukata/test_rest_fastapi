from typing import List
from fastapi import Depends, HTTPException, Request, Response, APIRouter

from dependencies import SessionDep, check_user_permission
from schemas import AccountResponse, PaymentResponse, UserLogin, UserResponse
from repository import AccountRepo, PaymentRepo, UserRepo


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login")
async def login(db: SessionDep, user: UserLogin, response: Response):
    """Авторизация через email/password"""
    check_user = await UserRepo.authenticate_user(db, user)
    if check_user is None:
        raise HTTPException(status_code=401,
                            detail='Неверная почта или пароль')

    response.set_cookie(key="user_id_from_cookie", value=str(check_user.id), expires=300, httponly=True)
    return {"message": "Успешный вход"}


@router.get("/{user_id_from_url}", response_model=UserResponse)
async def get_user(
    db: SessionDep,
    user_id_from_url: int,
    is_permission: bool = Depends(check_user_permission)
):
    db_user = await UserRepo.get_user_by_id(db, user_id_from_url)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return UserResponse.model_validate(db_user)


@router.get("/{user_id_from_url}/accounts", response_model=List[AccountResponse])
async def get_accounts(
    db: SessionDep,
    user_id_from_url: int,
    is_permission: bool = Depends(check_user_permission)
):
    return await AccountRepo.get_accounts(db, user_id_from_url, AccountResponse)


@router.get("/{user_id_from_url}/payments", response_model=List[PaymentResponse])
async def get_payments(
    db: SessionDep,
    user_id_from_url: int,
    is_permission: bool = Depends(check_user_permission)
):
    return await PaymentRepo.get_payments(db, user_id_from_url, PaymentResponse)
