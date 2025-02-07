from sqlalchemy import select
from auth import hash_password, verify_password
from db import SessionDep
from models import UserORM
from schemas import UserLogin, UserResponse, UserCreate, UserUpdate


# class UserRepository:
#     @staticmethod
#     async def create_user(db: SessionDep, email: str, password: str, full_name: str, is_admin: int = 0):
#         new_user = User(email=email, password=password, full_name=full_name, is_admin=is_admin)
#         session.add(new_user)
#         await session.commit()
#         return new_user

#     @staticmethod
#     async def get_user_by_id(db: SessionDep, user_id: int):
#         result = await session.execute(select(User).where(User.id == user_id))
#         return result.scalar()

#     @staticmethod
#     async def get_all_users(db: SessionDep):
#         result = await session.execute(select(User))
#         return result.scalars().all()

#     @staticmethod
#     async def update_user(db: SessionDep, user_id: int, email: str = None, full_name: str = None, is_admin: int = None):
#         user = await UserRepository.get_user_by_id(session, user_id)
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

    # @staticmethod
    # async def delete_user(db: SessionDep, user_id: int):
    #     user = await UserRepository.get_user_by_id(session, user_id)
    #     if not user:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     await session.delete(user)
    #     await session.commit()
    #     return {"message": "User deleted"}

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


async def update_user(db: SessionDep, user_id: int, user: UserUpdate):
    existing_user = await get_user_by_id(db, user_id)
    if not existing_user:
        return None
    
    existing_user.e
    

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
    user = result.scalars().first()
    if not user:
        return None
    return user


async def get_user_by_id(db: SessionDep, user: UserResponse, user_id: int) -> UserResponse:
    result = await db.execute(select(UserORM).where(UserORM.id == user_id))
    found_user = user.model_validate(result.scalars().first())
    return found_user


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