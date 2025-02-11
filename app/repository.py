from sqlalchemy import select
from auth import hash_password, verify_password
from db import SessionDep
from models import UserORM
from schemas import UserLogin, UserResponse, UserCreate, UserUpdate


class UserRepo:

    @staticmethod
    async def create_user(db: SessionDep, user: UserCreate) -> UserORM:
        existing_user = await UserRepo.get_user_by_email(db, user.email)
        if existing_user:
            return None

        new_user = UserORM(
            email=user.email, full_name=user.full_name, password=hash_password(user.password)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    
    @staticmethod
    async def update_user(db: SessionDep, user: UserUpdate, user_id: int) -> UserORM:
        existed_user = await UserRepo.get_user_by_id(db, user_id)
        if not existed_user:
            return None
        existed_user.email = user.email
        existed_user.full_name = user.full_name
        await db.commit()
        await db.refresh(existed_user)
        return existed_user

    @staticmethod
    async def delete_user(db: SessionDep, user_id: int) -> dict:
        user = await UserRepo.get_user_by_id(db, user_id)
        if not user:
            return None
        await db.delete(user)
        await db.commit()
        return {"message": "User deleted"}

    @staticmethod   
    async def authenticate_user(db: SessionDep, user: UserLogin):
        check_user = await UserRepo.get_user_by_email(db, user.email)
        if not check_user or verify_password(user.password, check_user.password) is False:
            return None
        return check_user

    @staticmethod
    async def get_user_by_id(db: SessionDep, user_id: int) -> UserORM:
        result = await db.execute(select(UserORM).where(UserORM.id == user_id))
        return result.scalar()

    @staticmethod
    async def get_user_by_email(db: SessionDep, email: str) -> UserORM:
        result = await db.execute(select(UserORM).where(UserORM.email == email))
        user = result.scalars().first()
        if not user:
            return None
        return user

    @staticmethod
    async def get_all_users(db: SessionDep, user: UserResponse) -> list[UserResponse]:
        result = await db.execute(select(UserORM))
        user_models = result.scalars().all()
        users = [user.model_validate(user_model) for user_model in user_models]
        return users
    

async def make_admin(db: SessionDep, user_id: int):
    admin = await db.get(UserORM, int(user_id))
    admin.is_admin = True
    await db.commit()
    return admin


async def check_admin(db: SessionDep, user_id: int) -> bool:
    user = await db.get(UserORM, int(user_id))
    if not user or not user.is_admin:
        return False
    return True

#     @staticmethod
#     async def update_user(db: SessionDep, user_id: int, email: str = None, full_name: str = None, is_admin: int = None):
#         user = await UserRepo.get_user_by_id(session, user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         if email:
#             user.email = email
#         if full_name:
#             user.full_name = full_name
#         if is_admin is not None:
#             user.is_admin = is_admin
#         await session.commit()
#         return user



# async def create_user(db: SessionDep, user: UserCreate):
#     existing_user = await get_user_by_email(db, user.email)
#     if existing_user:
#         return None

#     new_user = UserORM(
#         email=user.email, full_name=user.full_name, password=hash_password(user.password)
#     )
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)
#     return new_user


# async def get_users(db: SessionDep, user: UserResponse) -> list[UserResponse]:
#     query = select(UserORM)
#     result = await db.execute(query)
#     user_models = result.scalars().all()
#     users = [user.model_validate(user_model) for user_model in user_models]
#     return users


# async def get_user_by_id(db: SessionDep, user: UserResponse, user_id: int) -> UserORM:
#     result = await db.execute(select(UserORM).where(UserORM.id == user_id))
#     found_user = user.model_validate(result.scalars().first())
#     return found_user

