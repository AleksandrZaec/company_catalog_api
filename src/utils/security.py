from src.config.settings import settings
from src.config.logger import logger
from fastapi import HTTPException, Header


async def verify_api_key(api_key: str = Header(..., alias="X-API-Key")) -> None:
    if api_key != settings.API_KEY:
        logger.warning(f"Invalid API key provided")
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )
