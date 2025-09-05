from __future__ import annotations

from flask import Flask, jsonify, request
from python_common import configure_logging, configure_tracing, instrument_flask, require_jwt

_carts: dict[str, list[dict]] = {}


def create_app() -> Flask:
    configure_logging()
    configure_tracing("cart-service")
    app = Flask(__name__)
    instrument_flask(app)

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok", "service": "cart-service"})

    @app.get("/cart")
    @require_jwt
    def get_cart():
        user = getattr(request, "user", {})
        items = _carts.get(user.get("sub"), [])
        return jsonify({"items": items})

    @app.post("/cart")
    @require_jwt
    def add_to_cart():
        user = getattr(request, "user", {})
        body = request.get_json(force=True, silent=True) or {}
        item = {"sku": body.get("sku"), "qty": int(body.get("qty", 1))}
        cart = _carts.setdefault(user.get("sub"), [])
        cart.append(item)
        return jsonify({"ok": True, "items": cart})

    @app.delete("/cart")
    @require_jwt
    def clear_cart():
        user = getattr(request, "user", {})
        _carts[user.get("sub")] = []
        return jsonify({"ok": True})

    return app

