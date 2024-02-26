import jwt
from datetime import datetime, timedelta
from decouple import config


SECRET_KEY = config("SECRET_KEY")

ALGORITHM = "HS256"


ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create an access token for the given data.

    Parameters:
    - data (dict): The data to be encoded in the token.
    - expires_delta (timedelta, optional): The expiration time delta for the token. If not provided, a default expiration time will be used.

    Returns:
    - str: The encoded access token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
