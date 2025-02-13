from sqlalchemy import select
from auth import hash_password, verify_password
from dependencies import SessionDep
from models import AccountORM, PaymentORM, UserORM
from schemas import AccountResponse, PaymentResponse, UserLogin, UserResponse, UserCreate, UserUpdate


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


class AccountRepo:

    @staticmethod
    async def get_accounts(db: SessionDep, user_id: int, AccountSchema: AccountResponse) -> list[AccountResponse]:
        result = await db.execute(select(AccountORM).where(AccountORM.user_id == user_id))
        account_models = result.scalars().all()
        accounts = [AccountSchema.model_validate(account_model) for account_model in account_models]
        return accounts
    
    @staticmethod
    async def create_account(db: SessionDep, user_id: int, AccountSchema: AccountResponse) -> AccountResponse:
        new_account = AccountORM(user_id=user_id, balance=0)
        db.add(new_account)
        await db.commit()
        return AccountSchema.model_validate(new_account)


class PaymentRepo:

    @staticmethod
    async def get_payments(db: SessionDep, user_id: int, PaymentSchema: PaymentResponse) -> list[PaymentResponse]:
        result = await db.execute(select(PaymentORM).where(PaymentORM.user_id == user_id))
        payment_models = result.scalars().all()
        payments = [PaymentSchema.model_validate(payment_model) for payment_model in payment_models]
        return payments
