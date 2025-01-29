from fastapi import Header, HTTPException
from .config import settings

async def get_api_key(api_key: str = Header(..., convert_underscores=False)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    return api_key 