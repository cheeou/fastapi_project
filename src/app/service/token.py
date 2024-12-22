from typing import Dict, Any

from fastapi import HTTPException, status

from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from zoneinfo import ZoneInfo as timezone
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
# REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


class TokenService:
    def __init__(self, secret_key: str = SECRET_KEY,
                 algorithm: str = ALGORITHM,
                 ):

        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire_date = datetime.now(timezone("Asia/Seoul")) + timedelta(minutes=1)
        to_encode.update({"exp": expire_date})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire_date = datetime.now(timezone("Asia/Seoul")) + timedelta(days=1)
        to_encode.update({"exp": expire_date})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[self.algorithm])
            exp = payload.get("exp")
            user_email = payload.get("sub")

            if exp is None or datetime.now(timezone("Asia/Seoul")).timestamp() > exp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            elif not user_email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )
            return payload

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

