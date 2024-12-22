from pydantic import BaseModel, EmailStr

class LoginDto(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    email: str
    message: str

