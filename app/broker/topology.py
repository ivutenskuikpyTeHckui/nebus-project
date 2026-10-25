import aio_pika

from app.broker.constants import (
    MAIN_QUEUE_ARGUMENTS,
    PAYMENTS_DLQ,
    PAYMENTS_DLQ_ROUTING_KEY,
    PAYMENTS_DLX,
    PAYMENTS_EXCHANGE,
    PAYMENTS_NEW_QUEUE,
    PAYMENTS_NEW_ROUTING_KEY,
    RETRY_DELAYS_MS,
    retry_queue_arguments,
    retry_queue_name,
)
from app.utilities.config import CONFIG


async def declare_topology() -> None:
    connection = await aio_pika.connect_robust(CONFIG.RABBITMQ.URL)
    channel = await connection.channel()
    payments_exchange = await channel.declare_exchange(
        PAYMENTS_EXCHANGE,
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )
    dlx = await channel.declare_exchange(
        PAYMENTS_DLX,
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )
    dlq = await channel.declare_queue(PAYMENTS_DLQ, durable=True)
    await dlq.bind(dlx, routing_key=PAYMENTS_DLQ_ROUTING_KEY)
    for delay_ms in RETRY_DELAYS_MS:
        await channel.declare_queue(
            retry_queue_name(delay_ms),
            durable=True,
            arguments=retry_queue_arguments(delay_ms),
        )
    main_queue = await channel.declare_queue(
        PAYMENTS_NEW_QUEUE,
        durable=True,
        arguments=MAIN_QUEUE_ARGUMENTS,
    )
    await main_queue.bind(payments_exchange, routing_key=PAYMENTS_NEW_ROUTING_KEY)
    await connection.close()
