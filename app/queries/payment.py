import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.databases.orm.payment import Payment
from app.models.exceptions import NotFoundException


async def get_payment(
    db: AsyncSession,
    payment_id: uuid.UUID,
    for_update: bool = False,
) -> Payment:
    statement = select(Payment).where(Payment.id == payment_id)
    if for_update:
        statement = statement.with_for_update()
    payment = (await db.execute(statement)).scalar_one_or_none()
    if payment is None:
        raise NotFoundException(
            "Payment not found",
            extra={"payment_id": str(payment_id)},
        )
    return payment


async def get_payment_by_idempotency_key(
    db: AsyncSession,
    idempotency_key: str,
) -> Payment | None:
    statement = select(Payment).where(Payment.idempotency_key == idempotency_key)
    return (await db.execute(statement)).scalar_one_or_none()
