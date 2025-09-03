from __future__ import annotations

from flask import Flask, jsonify, request
from python_common import configure_logging, configure_tracing, instrument_flask

_products = {
    "sku-1": {"sku": "sku-1", "name": "T-Shirt", "price": 19.99},
    "sku-2": {"sku": "sku-2", "name": "Hoodie", "price": 49.99},
}


def create_app() -> Flask:
    configure_logging()
    configure_tracing("catalog-service")
    app = Flask(__name__)
    instrument_flask(app)

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok", "service": "catalog-service"})

    @app.get("/products")
    def list_products():
        return jsonify({"items": list(_products.values())})

    @app.get("/products/<sku>")
    def get_product(sku: str):
        product = _products.get(sku)
        if not product:
            return jsonify({"error": "not_found"}), 404
        return jsonify(product)

    return app

