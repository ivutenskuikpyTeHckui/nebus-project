import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import Field, field_serializer

from app.models.databases.orm.payment import Payment
from app.models.enums.payment import PaymentStatus
from app.models.pydantic_schemas.base import ResponseModel


class CreatePaymentResponseModel(ResponseModel):
    payment_id: uuid.UUID
    status: PaymentStatus
    created_at: datetime

    @classmethod
    def from_orm_payment(cls, payment: Payment) -> "CreatePaymentResponseModel":
        return cls(
            payment_id=payment.id,
            status=payment.status,
            created_at=payment.created_at,
        )


class PaymentResponseModel(ResponseModel):
    payment_id: uuid.UUID
    amount: Decimal
    currency: str
    description: str
    metadata_json: dict = Field(alias="metadata")
    status: PaymentStatus
    idempotency_key: str
    webhook_url: str
    created_at: datetime
    processed_at: datetime | None

    @field_serializer("amount")
    def serialize_amount(self, value: Decimal) -> str:
        return f"{value:.2f}"

    @classmethod
    def from_orm_payment(cls, payment: Payment) -> "PaymentResponseModel":
        return cls(
            payment_id=payment.id,
            amount=payment.amount,
            currency=payment.currency,
            description=payment.description,
            metadata=payment.metadata_json,
            status=payment.status,
            idempotency_key=payment.idempotency_key,
            webhook_url=payment.webhook_url,
            created_at=payment.created_at,
            processed_at=payment.processed_at,
        )
