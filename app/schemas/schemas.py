from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# -----------------------------
# User Schemas
# -----------------------------

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
