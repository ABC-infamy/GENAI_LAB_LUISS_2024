from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

async def authenticate(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Please sign in"
        )
    payload = verify_access_token(token)
    return payload["user"]