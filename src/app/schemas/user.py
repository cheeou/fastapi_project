from pydantic import BaseModel, EmailStr

class CurrenUserResponse(BaseModel):
    email: EmailStr