import asyncio

from faststream.rabbit import RabbitBroker, RabbitExchange

from app.databases.client_postgresql import async_session_maker
from app.queries.outbox import get_unpublished_outbox, mark_outbox_published
from app.utilities.logger import logger

POLL_INTERVAL_SECONDS = 1


async def publish_outbox_batch(
    broker: RabbitBroker,
    exchange: RabbitExchange,
) -> None:
    async with async_session_maker() as session:
        async with session.begin():
            rows = await get_unpublished_outbox(db=session, limit=20)
            for row in rows:
                await broker.publish(
                    row.payload,
                    exchange=exchange,
                    routing_key="payments.new",
                )
                mark_outbox_published(row)
                logger.debug(
                    "Outbox published",
                    extra={
                        "outbox_id": str(row.id),
                        "aggregate_id": str(row.aggregate_id),
                    },
                )


async def outbox_relay_loop(
    broker: RabbitBroker,
    exchange: RabbitExchange,
) -> None:
    while True:
        try:
            await publish_outbox_batch(broker=broker, exchange=exchange)
        except Exception as exc:
            logger.error("Outbox relay failed", extra={"error": str(exc)})
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
