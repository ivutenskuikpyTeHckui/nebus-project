from app.models.enums.base import StrEnumModel


class PaymentCurrency(StrEnumModel):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class PaymentStatus(StrEnumModel):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
