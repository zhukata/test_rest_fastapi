from typing import Annotated
from fastapi import Cookie, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserORM
from db import get_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user_id(request: Request):
    user_id = request.cookies.get("user_id_from_cookie")
    if not user_id:
        raise HTTPException(status_code=401, detail="Необходимо авторизоваться")
    return user_id


async def check_admin(db: SessionDep, user_id: int) -> bool:
    user = await db.get(UserORM, int(user_id))
    if not user or not user.is_admin:
        return False
    return True


async def admin_required(
    db: SessionDep,
    user_id_from_cookie: int = Depends(get_current_user_id) 
):
    """Проверка, является ли пользователь администратором"""
    if not await check_admin(db, user_id_from_cookie):
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return True
