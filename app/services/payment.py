import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.databases.orm.outbox import Outbox
from app.models.databases.orm.payment import Payment
from app.models.enums.payment import PaymentStatus
from app.models.exceptions import ConflictException
from app.models.request_models.payment import CreatePaymentRequestModel
from app.queries.payment import get_payment, get_payment_by_idempotency_key
from app.services.idempotency import build_request_hash, normalize_amount
from app.utilities.logger import logger

EVENT_TYPE_PAYMENT_CREATED = "payment.created"


def _same_request(payment: Payment, request_hash: str) -> Payment:
    if payment.request_hash != request_hash:
        raise ConflictException(
            "Idempotency key already used with a different payload",
            extra={
                "idempotency_key": payment.idempotency_key,
                "payment_id": str(payment.id),
            },
        )
    return payment


async def create_payment(
    db: AsyncSession,
    payload: CreatePaymentRequestModel,
    idempotency_key: str,
) -> Payment:
    request_hash = build_request_hash(payload)
    existing = await get_payment_by_idempotency_key(
        db=db,
        idempotency_key=idempotency_key,
    )
    if existing is not None:
        logger.debug(
            "Idempotent payment replay",
            extra={"payment_id": str(existing.id)},
        )
        return _same_request(existing, request_hash)

    amount = normalize_amount(payload.amount)
    payment = Payment(
        amount=amount,
        currency=payload.currency,
        description=payload.description,
        metadata_json=payload.metadata_json,
        status=PaymentStatus.PENDING.value,
        idempotency_key=idempotency_key,
        webhook_url=str(payload.webhook_url),
        request_hash=request_hash,
    )
    db.add(payment)
    await db.flush()
    db.add(
        Outbox(
            aggregate_type="payment",
            aggregate_id=payment.id,
            event_type=EVENT_TYPE_PAYMENT_CREATED,
            payload={
                "payment_id": str(payment.id),
                "amount": f"{amount:.2f}",
                "currency": payload.currency,
                "webhook_url": str(payload.webhook_url),
                "idempotency_key": idempotency_key,
            },
        )
    )
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raced = await get_payment_by_idempotency_key(
            db=db,
            idempotency_key=idempotency_key,
        )
        if raced is None:
            raise
        return _same_request(raced, request_hash)

    logger.debug("Payment Created", extra={"payment_id": str(payment.id)})
    return payment


async def get_payment_details(db: AsyncSession, payment_id: uuid.UUID) -> Payment:
    return await get_payment(db=db, payment_id=payment_id)
