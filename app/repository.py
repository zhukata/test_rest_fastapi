from sqlalchemy import select

from app.auth import hash_password, verify_password
from app.dependencies import SessionDep
from app.models import AccountORM, PaymentORM, UserORM
from app.schemas import AccountResponse, PaymentResponse
from app.schemas import UserLogin, UserResponse, UserCreate, UserUpdate


class UserRepo:

    @staticmethod
    async def create_user(db: SessionDep, user: UserCreate) -> UserORM | None:
        existing_user = await UserRepo.get_user_by_email(db, user.email)
        if existing_user:
            return None

        new_user = UserORM(
            email=user.email,
            full_name=user.full_name,
            password=hash_password(user.password)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def update_user(
        db: SessionDep,
        user: UserUpdate,
        user_id: int
    ) -> UserORM | None:
        user_data = user.model_dump(exclude_unset=True)

        if not user_data:
            return None  

        existed_user = await UserRepo.get_user_by_id(db, user_id)
        if not existed_user:
            return None

        for key, value in user_data.items():
            setattr(existed_user, key, value)

        await db.commit()
        await db.refresh(existed_user)
        return existed_user

    @staticmethod
    async def delete_user(db: SessionDep, user_id: int) -> bool:
        user = await UserRepo.get_user_by_id(db, user_id)
        if not user:
            return False
        await db.delete(user)
        await db.commit()
        return True

    @staticmethod
    async def authenticate_user(
        db: SessionDep,
        user: UserLogin
    ) -> UserORM | None:
        check_user = await UserRepo.get_user_by_email(db, user.email)
        if not check_user or not verify_password(
            user.password,
            check_user.password
        ):
            return None
        return check_user

    @staticmethod
    async def get_user_by_id(db: SessionDep, user_id: int) -> UserORM | None:
        result = await db.execute(select(UserORM).where(UserORM.id == user_id))
        return result.scalar()

    @staticmethod
    async def get_user_by_email(db: SessionDep, email: str) -> UserORM | None:
        result = await db.execute(
            select(UserORM).where(UserORM.email == email)
        )
        return result.scalars().first()

    @staticmethod
    async def get_all_users(
        db: SessionDep,
        user_schema: UserResponse
    ) -> list[UserResponse]:
        result = await db.execute(select(UserORM))
        user_models = result.scalars().all()
        users = [
            user_schema.model_validate(user_model)
            for user_model in user_models
        ]
        return users


class AccountRepo:

    @staticmethod
    async def get_accounts(
        db: SessionDep,
        user_id: int,
        account_schema: AccountResponse
    ) -> list[AccountResponse]:
        result = await db.execute(
            select(AccountORM).where(AccountORM.user_id == user_id)
        )
        account_models = result.scalars().all()
        accounts = [
            account_schema.model_validate(account_model)
            for account_model in account_models
        ]
        return accounts

    @staticmethod
    async def create_account(
        db: SessionDep,
        user_id: int,
        account_schema: AccountResponse
    ) -> AccountResponse:
        new_account = AccountORM(user_id=user_id, balance=0)
        db.add(new_account)
        await db.commit()
        await db.refresh(new_account)
        return account_schema.model_validate(new_account)


class PaymentRepo:

    @staticmethod
    async def get_payments(
        db: SessionDep,
        user_id: int,
        PaymentSchema: PaymentResponse
    ) -> list[PaymentResponse]:
        result = await db.execute(
            select(PaymentORM).where(PaymentORM.user_id == user_id)
        )
        payment_models = result.scalars().all()
        payments = [
            PaymentSchema.model_validate(payment_model)
            for payment_model in payment_models
        ]
        return payments
