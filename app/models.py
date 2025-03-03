from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, text

from app.db import Base


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(
        default=False,
        server_default=text('false'),
        nullable=False
    )
    
    accounts = relationship("AccountORM", back_populates="user", cascade="all, delete-orphan")



class AccountORM(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    balance: Mapped[float] = mapped_column(Integer, server_default=text('0'))

    user = relationship("UserORM", back_populates="accounts")

class PaymentORM(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_id: Mapped[int] = mapped_column(
        String,
        unique=True,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    account_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )
    amount: Mapped[float] = mapped_column(Integer, nullable=False)
