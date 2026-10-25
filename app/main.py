import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.broker.rabbit import broker, payments_exchange
from app.broker.topology import declare_topology
from app.models.exceptions import LogicException
from app.models.response_models.exceptions import (
    ExceptionHandler,
    LogicExceptionHandler,
    RequestValidationErrorHandler,
)
from app.routes.payment import router as payment_router
from app.services.outbox_relay import outbox_relay_loop

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await declare_topology()
    await broker.start()
    relay_task = asyncio.create_task(
        outbox_relay_loop(broker=broker, exchange=payments_exchange)
    )
    try:
        yield
    finally:
        relay_task.cancel()
        await broker.close()


app = FastAPI(
    title="Payment processing",
    lifespan=lifespan,
    exception_handlers={
        LogicException: LogicExceptionHandler.handler,
        RequestValidationError: RequestValidationErrorHandler.handler,
        Exception: ExceptionHandler.handler,
    },
)

app.include_router(payment_router, prefix="/api/v1/payments", tags=["payments"])
