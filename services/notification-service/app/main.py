from __future__ import annotations

from flask import Flask, jsonify
from python_common import configure_logging, configure_tracing, instrument_flask


def create_app() -> Flask:
    configure_logging()
    configure_tracing("notification-service")
    app = Flask(__name__)
    instrument_flask(app)

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok", "service": "notification-service"})

    return app

