from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ReferenceImage(BaseModel):
    id: int
    user_id: int
    image_data: bytes

    class Config:
        orm_mode = True

class VerificationResult(BaseModel):
    verified: bool
    distance: float
    threshold: float
    model: str
    detector_backend: str