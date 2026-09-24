import hashlib
import hmac
import json
import os
import time
import urllib.parse

from fastapi import Header, HTTPException

from config import config


def validate_init_data(init_data: str, bot_token: str) -> dict:
    if not init_data:
        raise ValueError("empty init data")

    data = dict(urllib.parse.parse_qsl(init_data, keep_blank_values=True))
    received_hash = data.pop("hash", None)
    if not received_hash:
        raise ValueError("missing hash")

    check_string = "\n".join(f"{k}={data[k]}" for k in sorted(data))

    secret_key = hmac.new(
        b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256
    ).digest()
    calculated_hash = hmac.new(
        secret_key, check_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError("bad signature")

    auth_date = int(data.get("auth_date", "0"))
    if time.time() - auth_date > 86400:
        raise ValueError("stale auth date")

    user_raw = data.get("user")
    if not user_raw:
        raise ValueError("no user in init data")

    return json.loads(user_raw)


async def current_user(
    x_telegram_init_data: str | None = Header(
        default=None, alias="X-Telegram-Init-Data"
    ),
) -> dict:
    if not x_telegram_init_data:
        if os.getenv("DEV_MODE") == "1":
            return {"id": 1, "first_name": "Dev", "last_name": "", "username": None}
        raise HTTPException(status_code=401, detail="Missing Telegram auth data")
    try:
        return validate_init_data(x_telegram_init_data, config.bot_token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Invalid auth: {exc}")
