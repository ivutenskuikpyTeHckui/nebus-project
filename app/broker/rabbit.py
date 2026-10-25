from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue

from app.broker.constants import (
    MAIN_QUEUE_ARGUMENTS,
    PAYMENTS_EXCHANGE,
    PAYMENTS_NEW_QUEUE,
    PAYMENTS_NEW_ROUTING_KEY,
)
from app.utilities.config import CONFIG

broker = RabbitBroker(CONFIG.RABBITMQ.URL)
payments_exchange = RabbitExchange(
    PAYMENTS_EXCHANGE,
    type=ExchangeType.DIRECT,
    durable=True,
)
payments_queue = RabbitQueue(
    PAYMENTS_NEW_QUEUE,
    durable=True,
    routing_key=PAYMENTS_NEW_ROUTING_KEY,
    arguments=MAIN_QUEUE_ARGUMENTS,
)
