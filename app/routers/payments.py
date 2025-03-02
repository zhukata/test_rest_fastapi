from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.schemas import PaymentWebhook
from app.auth import generate_signature
from app.dependencies import SessionDep
from app.models import AccountORM, PaymentORM


router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/webhook")
async def process_webhook(payment: PaymentWebhook, db: SessionDep):
    """Эмуляция вебхука, сохранение платежа в бд"""
    computed_signature = generate_signature(
        payment.account_id,
        payment.amount,
        payment.transaction_id,
        payment.user_id
    )
    if computed_signature != payment.signature:
        raise HTTPException(status_code=400, detail="Неверная подпись")

    async with db.begin():
        existing_payment = await db.execute(
            select(PaymentORM).where(
                PaymentORM.transaction_id == payment.transaction_id))
        if existing_payment.scalar():
            raise HTTPException(
                status_code=400,
                detail="Транзакция уже в процессе"
            )

        account = await db.execute(
            select(AccountORM).where(AccountORM.id == payment.account_id))
        account = account.scalar()
        if not account:
            raise HTTPException(status_code=404, detail="Счет не найден")

        new_payment = PaymentORM(
            transaction_id=payment.transaction_id,
            user_id=payment.user_id,
            account_id=payment.account_id,
            amount=payment.amount
        )
        account.balance += payment.amount
        db.add(new_payment)
        db.add(account)
        await db.commit()

    return {"message": "Платеж совершен"}
