PAYMENTS_EXCHANGE = "payments"
PAYMENTS_DLX = "payments.dlx"
PAYMENTS_NEW_QUEUE = "payments.new"
PAYMENTS_NEW_ROUTING_KEY = "payments.new"
PAYMENTS_DLQ = "payments.new.dlq"
PAYMENTS_DLQ_ROUTING_KEY = "payments.new.dlq"
MAX_ATTEMPTS = 3
RETRY_DELAYS_MS = (1000, 2000)
MAIN_QUEUE_ARGUMENTS = {
    "x-dead-letter-exchange": PAYMENTS_DLX,
    "x-dead-letter-routing-key": PAYMENTS_DLQ_ROUTING_KEY,
}


def retry_queue_name(delay_ms: int) -> str:
    return f"payments.new.retry.{delay_ms}"


def retry_queue_arguments(delay_ms: int) -> dict:
    return {
        "x-message-ttl": delay_ms,
        "x-dead-letter-exchange": PAYMENTS_EXCHANGE,
        "x-dead-letter-routing-key": PAYMENTS_NEW_ROUTING_KEY,
    }
