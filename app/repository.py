from fastapi import HTTPException
from sqlalchemy import select
from auth import hash_password
from db import SessionDep
from models import UserORM
from schemas import UserResponse, UserCreate


async def create_user(db: SessionDep, user: UserCreate):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User уже зарегистрирован")

    new_user = UserORM(
        email=user.email, full_name=user.full_name, password=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_users(db: SessionDep, user: UserResponse) -> list[UserResponse]:
    query = select(UserORM)
    result = await db.execute(query)
    user_models = result.scalars().all()
    users = [user.model_validate(user_model) for user_model in user_models]
    return users


async def get_user_by_email(db: SessionDep, email: str):
    result = await db.execute(select(UserORM).where(UserORM.email == email))
    return result.scalars().first()


async def get_user_by_id(db: SessionDep, user_id: int):
    result = await db.execute(select(UserORM).where(UserORM.id == user_id))
    return result.scalars().first()