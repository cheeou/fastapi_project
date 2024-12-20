from pydantic import BaseModel, EmailStr, Field, ValidationError
from typing_extensions import Self

class EmailDto(BaseModel):
    email: EmailStr

class RegisterDto(EmailDto):
    password1: str = Field(min_length=8, max_length=30, serialization_alias="password")
    password2: str = Field(min_length=8, max_length=30, exclude=True)

    def check_pwd_match(self) -> Self:
        password1 = self.password1
        password2 = self.password2

        if password1 is not None and password2 is not None and password1 != password2:
            raise ValidationError("Passwords don't match")
        return Self