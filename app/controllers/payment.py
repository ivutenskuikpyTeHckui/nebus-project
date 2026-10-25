import uuid

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request_models.payment import CreatePaymentRequestModel
from app.models.response_models.payment import (
    CreatePaymentResponseModel,
    PaymentResponseModel,
)
from app.services.payment import create_payment as service_create_payment
from app.services.payment import get_payment_details
from app.utilities.dependecies.authentication import get_api_key
from app.utilities.dependecies.database import get_async_db
from app.utilities.logger import logger


async def create_payment(
    payload: CreatePaymentRequestModel,
    idempotency_key: str = Header(
        alias="Idempotency-Key",
        min_length=1,
        max_length=255,
    ),
    _: str = Depends(get_api_key),
    db: AsyncSession = Depends(get_async_db),
) -> CreatePaymentResponseModel:
    logger.debug(
        "Payload Received",
        extra={
            "payload": payload.model_dump(mode="json"),
            "idempotency_key": idempotency_key,
        },
    )
    payment = await service_create_payment(
        db=db,
        payload=payload,
        idempotency_key=idempotency_key,
    )
    return CreatePaymentResponseModel.from_orm_payment(payment)


async def get_payment(
    payment_id: uuid.UUID,
    _: str = Depends(get_api_key),
    db: AsyncSession = Depends(get_async_db),
) -> PaymentResponseModel:
    logger.debug("Payload Received", extra={"payment_id": str(payment_id)})
    payment = await get_payment_details(db=db, payment_id=payment_id)
    return PaymentResponseModel.from_orm_payment(payment)
