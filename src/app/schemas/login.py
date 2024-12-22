from typing import Self

from pydantic import BaseModel, EmailStr, Field, model_validator

class LoginDto(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    email: str
    message: str

