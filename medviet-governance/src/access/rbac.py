"""Casbin RBAC helpers for the MedViet FastAPI service."""
from __future__ import annotations

from functools import wraps
from pathlib import Path
from typing import Optional

import casbin
from fastapi import Header, HTTPException

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.conf"
POLICY_PATH = BASE_DIR / "policy.csv"

MOCK_USERS = {
    "token-alice": {"username": "alice", "role": "admin"},
    "token-bob": {"username": "bob", "role": "ml_engineer"},
    "token-carol": {"username": "carol", "role": "data_analyst"},
    "token-dave": {"username": "dave", "role": "intern"},
}

enforcer = casbin.Enforcer(str(MODEL_PATH), str(POLICY_PATH))


def get_current_user(authorization: Optional[str] = Header(None)) -> dict[str, str]:
    """Parse a Bearer token and return mock user information."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.split(" ", 1)[1].strip()
    user = MOCK_USERS.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


def require_permission(resource: str, action: str):
    """Decorator that checks role permission with Casbin."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(status_code=401, detail="Missing authenticated user")

            role = current_user["role"]
            allowed = enforcer.enforce(role, resource, action)
            if not allowed:
                raise HTTPException(
                    status_code=403,
                    detail=f"Role '{role}' cannot '{action}' on '{resource}'",
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator
