import hashlib
import json
from decimal import Decimal

from app.models.request_models.payment import CreatePaymentRequestModel


def normalize_amount(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal("0.01"))


def build_request_hash(payload: CreatePaymentRequestModel) -> str:
    canonical = {
        "amount": str(normalize_amount(payload.amount)),
        "currency": payload.currency,
        "description": payload.description,
        "metadata": payload.metadata_json,
        "webhook_url": str(payload.webhook_url),
    }
    raw = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
