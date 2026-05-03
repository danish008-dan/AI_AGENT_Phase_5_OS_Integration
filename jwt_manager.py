# os_layer/security/confirmation_manager.py


import jwt
import os
from fastapi import HTTPException

SECRET = os.getenv("JWT_SECRET", "CHANGE_THIS_SECRET")

def decode_token(token: str):

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")