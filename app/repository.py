from sqlalchemy import select
from auth import hash_password, verify_password
from db import SessionDep
from models import UserORM
from schemas import UserLogin, UserResponse, UserCreate


async def create_user(db: SessionDep, user: UserCreate):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        return None

    new_user = UserORM(
        email=user.email, full_name=user.full_name, password=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def authenticate_user(db: SessionDep, user: UserLogin):
    check_user = await get_user_by_email(db, user.email)
    if not check_user or verify_password(user.password, check_user.password) is False:
        return None
    return check_user

async def get_users(db: SessionDep, user: UserResponse) -> list[UserResponse]:
    query = select(UserORM)
    result = await db.execute(query)
    user_models = result.scalars().all()
    users = [user.model_validate(user_model) for user_model in user_models]
    return users


async def get_user_by_email(db: SessionDep, email: str) -> UserORM:
    result = await db.execute(select(UserORM).where(UserORM.email == email))
    return result.scalars().first()


async def get_user_by_id(db: SessionDep, user: UserResponse, user_id: int) -> UserResponse:
    result = await db.execute(select(UserORM).where(UserORM.id == user_id))
    found_user = user.model_validate(result.scalars().first())
    return found_user


async def make_admin(db: SessionDep, user_id: int):
    admin = await db.get(UserORM, user_id)
    admin.is_admin = True
    await db.commit()
    return admin


async def check_admin(db: SessionDep, user_id: int) -> bool:
    user = await db.get(UserORM, user_id)
    if user.is_admin:
        return True