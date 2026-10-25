from decimal import Decimal

from pydantic import Field, HttpUrl

from app.models.enums.payment import PaymentCurrency
from app.models.pydantic_schemas.base import RequestModel


class CreatePaymentRequestModel(RequestModel):
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    currency: PaymentCurrency
    description: str = Field(min_length=1, max_length=2000)
    metadata_json: dict = Field(default_factory=dict, alias="metadata")
    webhook_url: HttpUrl
