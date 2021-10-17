import asyncio
import signal
from typing import Any

from hypercorn.asyncio import serve
from hypercorn.config import Config

from ibans.app import app


config = Config()
config.bind = ["localhost:8000"]
shutdown_event = asyncio.Event()


def _signal_handler(*_: Any) -> None:
    shutdown_event.set()


loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGTERM, _signal_handler)

try:
    loop.run_until_complete(serve(app, config, shutdown_trigger=shutdown_event.wait))
except KeyboardInterrupt:
    pass
