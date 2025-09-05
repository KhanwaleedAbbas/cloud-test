from __future__ import annotations

import logging
import time

from python_common import configure_logging, configure_tracing, receive_messages


def handle_event(event: dict) -> None:
    event_type = event.get("type")
    payload = event.get("payload", {})
    logging.getLogger("notification-worker").info("event", extra={"type": event_type, "payload": payload})


def main() -> None:
    configure_logging()
    configure_tracing("notification-worker")
    while True:
        receive_messages(handler=handle_event)
        time.sleep(1)


if __name__ == "__main__":
    main()

