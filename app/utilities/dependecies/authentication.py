import secrets

from fastapi import Header

from app.models.exceptions import UnauthorizedException
from app.utilities.config import CONFIG


async def get_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> str:
    expected = CONFIG.AUTH.API_KEY
    if x_api_key is None or not secrets.compare_digest(x_api_key, expected):
        raise UnauthorizedException("Invalid API key")
    return x_api_key
