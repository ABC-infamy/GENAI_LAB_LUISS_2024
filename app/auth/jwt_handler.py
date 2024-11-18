from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY=os.getenv('SECRET_KEY')

def create_access_token(data: dict):
    #data "user - username , expire - expiration date" passing dict already
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise JWTError("Invalid token")
