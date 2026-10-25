import uuid

from faststream.rabbit import Channel, RabbitMessage

from app.broker.constants import (
    MAX_ATTEMPTS,
    PAYMENTS_DLQ,
    PAYMENTS_DLX,
    RETRY_DELAYS_MS,
    retry_queue_name,
)
from app.broker.rabbit import broker, payments_exchange, payments_queue
from app.models.exceptions import NotFoundException
from app.services.payment_processing import process_payment
from app.utilities.logger import logger


def _attempt(message: RabbitMessage) -> int:
    headers = dict(message.headers or {})
    try:
        return int(headers.get("x-retry-count", 1))
    except (TypeError, ValueError):
        return 1


async def _publish_dlq(body: dict, attempt: int, error: str) -> None:
    await broker.publish(
        body,
        exchange=PAYMENTS_DLX,
        routing_key=PAYMENTS_DLQ,
        headers={"x-retry-count": attempt, "x-error": error[:500]},
    )
    logger.error(
        "Payment message sent to DLQ",
        extra={"attempt": attempt, "error": error},
    )


async def _schedule_retry(body: dict, attempt: int) -> None:
    delay_ms = RETRY_DELAYS_MS[attempt - 1]
    await broker.publish(
        body,
        queue=retry_queue_name(delay_ms),
        headers={"x-retry-count": attempt + 1},
    )
    logger.error(
        "Payment message scheduled for retry",
        extra={"attempt": attempt, "delay_ms": delay_ms},
    )


@broker.subscriber(
    payments_queue,
    payments_exchange,
    channel=Channel(prefetch_count=1),
)
async def on_payment_new(body: dict, message: RabbitMessage) -> None:
    attempt = _attempt(message)
    logger.debug(
        "Payment message received",
        extra={"body": body, "attempt": attempt},
    )
    try:
        payment_id = uuid.UUID(str(body["payment_id"]))
    except (KeyError, ValueError, TypeError) as exc:
        await _publish_dlq(
            body=body,
            attempt=attempt,
            error=f"invalid payload: {exc}",
        )
        return
    try:
        await process_payment(payment_id)
    except NotFoundException as exc:
        await _publish_dlq(body=body, attempt=attempt, error=str(exc))
    except Exception as exc:
        if attempt >= MAX_ATTEMPTS:
            await _publish_dlq(body=body, attempt=attempt, error=str(exc))
            return
        await _schedule_retry(body=body, attempt=attempt)
