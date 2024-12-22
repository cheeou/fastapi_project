from typing import Self

from pydantic import BaseModel, EmailStr, Field, model_validator

class EmailDto(BaseModel):
    email: EmailStr

class RegisterDto(EmailDto):
    password1: str = Field(min_length=8, max_length=30, serialization_alias="password")
    password2: str = Field(min_length=8, max_length=30)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        pw1 = self.password1
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self

class RegisterResponse(BaseModel):
    email: str
    message: str