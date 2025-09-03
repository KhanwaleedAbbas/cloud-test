from __future__ import annotations

from flask import Flask, jsonify, request
from python_common import configure_logging, configure_tracing, instrument_flask
from python_common import encode_jwt_token, require_jwt


def create_app() -> Flask:
    configure_logging()
    configure_tracing("auth-service")
    app = Flask(__name__)
    instrument_flask(app)

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok", "service": "auth-service"})

    @app.post("/auth/token")
    def issue_token():
        body = request.get_json(force=True, silent=True) or {}
        user_id = body.get("user_id", "user-1")
        email = body.get("email", "user@example.com")
        payload = {"sub": user_id, "email": email, "roles": ["user"]}
        token = encode_jwt_token(payload)
        return jsonify({"access_token": token})

    @app.get("/auth/me")
    @require_jwt
    def me():
        user = getattr(request, "user", {})
        return jsonify(user)

    return app

