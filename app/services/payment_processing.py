import uuid
from datetime import datetime, timezone

from app.databases.client_postgresql import async_session_maker
from app.models.enums.payment import PaymentStatus
from app.queries.payment import get_payment
from app.services.gateway import emulate_gateway
from app.services.webhook import send_webhook
from app.utilities.logger import logger


async def process_payment(payment_id: uuid.UUID) -> None:
    async with async_session_maker() as session:
        async with session.begin():
            payment = await get_payment(
                db=session,
                payment_id=payment_id,
                for_update=True,
            )
            if payment.status == PaymentStatus.PENDING.value:
                succeeded = await emulate_gateway()
                payment.status = (
                    PaymentStatus.SUCCEEDED.value
                    if succeeded
                    else PaymentStatus.FAILED.value
                )
                payment.processed_at = datetime.now(timezone.utc)
                logger.debug(
                    "Payment processed",
                    extra={
                        "payment_id": str(payment.id),
                        "status": payment.status,
                    },
                )
            body = {
                "payment_id": str(payment.id),
                "status": payment.status,
                "amount": f"{payment.amount:.2f}",
                "currency": payment.currency,
                "processed_at": (
                    payment.processed_at.isoformat() if payment.processed_at else None
                ),
            }
            webhook_url = payment.webhook_url
    await send_webhook(url=webhook_url, payload=body)
