from __future__ import annotations

from flask import Flask, jsonify, request
from python_common import configure_logging, configure_tracing, instrument_flask
from python_common import publish_event


def create_app() -> Flask:
    configure_logging()
    configure_tracing("payment-service")
    app = Flask(__name__)
    instrument_flask(app)

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok", "service": "payment-service"})

    @app.post("/payments")
    def capture():
        body = request.get_json(force=True, silent=True) or {}
        order_id = body.get("order_id")
        amount = body.get("amount", 0.0)
        payment = {"payment_id": order_id, "amount": amount, "status": "captured"}
        publish_event("payment.captured", payment)
        return jsonify(payment), 201

    return app

