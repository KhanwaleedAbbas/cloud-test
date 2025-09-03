from __future__ import annotations

import os
import requests
from flask import Flask, jsonify, request
from python_common import configure_logging, configure_tracing, instrument_flask, require_jwt
from python_common import publish_event


def create_app() -> Flask:
    configure_logging()
    configure_tracing("order-service")
    app = Flask(__name__)
    instrument_flask(app)

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok", "service": "order-service"})

    @app.post("/orders")
    @require_jwt
    def create_order():
        body = request.get_json(force=True, silent=True) or {}
        user = getattr(request, "user", {})
        # very naive pricing: fetch each SKU from catalog
        items = body.get("items", [])
        total = 0.0
        for item in items:
            sku = item.get("sku")
            qty = int(item.get("qty", 1))
            r = requests.get(f"http://catalog-service:8000/products/{sku}")
            if r.status_code != 200:
                return jsonify({"error": "invalid_sku", "sku": sku}), 400
            price = r.json().get("price", 0.0)
            total += price * qty

        order = {
            "order_id": os.urandom(4).hex(),
            "user_id": user.get("sub"),
            "items": items,
            "total": round(total, 2),
            "status": "created",
        }

        publish_event("order.created", order)
        return jsonify(order), 201

    return app

