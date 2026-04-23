from pydantic import BaseModel, Field
from typing import Optional


class BaseUser(BaseModel):
    username: str = Field(min_length=3)
    email: Optional[str] = None
    role:Optional[str]="user"

class UserCreate(BaseUser):
    password: str = Field(min_length=6)


class UserPublic(BaseUser):
    id: int

    class Config:
        from_attributes = True