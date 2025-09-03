from __future__ import annotations

from flask import Flask, jsonify
from python_common import configure_logging, configure_tracing, instrument_flask

_stock = {
    "sku-1": 100,
    "sku-2": 50,
}


def create_app() -> Flask:
    configure_logging()
    configure_tracing("inventory-service")
    app = Flask(__name__)
    instrument_flask(app)

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok", "service": "inventory-service"})

    @app.get("/inventory/<sku>")
    def get_inventory(sku: str):
        qty = _stock.get(sku, 0)
        return jsonify({"sku": sku, "qty": qty})

    return app

