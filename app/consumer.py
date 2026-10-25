import asyncio
import logging

from faststream import FastStream

from app.broker.rabbit import broker
from app.broker.topology import declare_topology
from app.consumers import payment as payment_consumer  # noqa: F401

logging.basicConfig(level=logging.INFO)

app = FastStream(broker)


@app.on_startup
async def on_startup() -> None:
    await declare_topology()


def main() -> None:
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
