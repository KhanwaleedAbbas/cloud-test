from __future__ import annotations

import os
import time
from functools import wraps
from typing import Callable, Any

import jwt
from flask import request, jsonify


def encode_jwt_token(payload: dict, ttl_seconds: int | None = None) -> str:
    secret = os.getenv("JWT_SECRET", "dev-secret")
    ttl = ttl_seconds or int(os.getenv("TOKEN_TTL_SECONDS", "3600"))
    now = int(time.time())
    body = {
        **payload,
        "iat": now,
        "exp": now + ttl,
    }
    return jwt.encode(body, secret, algorithm="HS256")


def decode_jwt_token(token: str) -> dict:
    secret = os.getenv("JWT_SECRET", "dev-secret")
    return jwt.decode(token, secret, algorithms=["HS256"])  # nosec - local dev only


def require_jwt(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "missing_or_invalid_token"}), 401
        token = auth_header.split(" ", 1)[1]
        try:
            request.user = decode_jwt_token(token)  # type: ignore[attr-defined]
        except Exception:
            return jsonify({"error": "invalid_token"}), 401
        return f(*args, **kwargs)

    return wrapper

