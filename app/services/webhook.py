import asyncio

import httpx

from app.utilities.config import CONFIG
from app.utilities.logger import logger


class WebhookDeliveryError(Exception):
    pass


async def send_webhook(url: str, payload: dict) -> None:
    delay_seconds = 1
    last_error = "unknown"
    async with httpx.AsyncClient(timeout=CONFIG.WEBHOOK.TIMEOUT_SECONDS) as client:
        for attempt in range(1, CONFIG.WEBHOOK.MAX_ATTEMPTS + 1):
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                logger.debug(
                    "Webhook delivered",
                    extra={"url": url, "attempt": attempt},
                )
                return
            except Exception as exc:
                last_error = str(exc)
                logger.error(
                    "Webhook delivery failed",
                    extra={"url": url, "attempt": attempt, "error": last_error},
                )
                if attempt < CONFIG.WEBHOOK.MAX_ATTEMPTS:
                    await asyncio.sleep(delay_seconds)
                    delay_seconds *= 2
    raise WebhookDeliveryError(last_error)
