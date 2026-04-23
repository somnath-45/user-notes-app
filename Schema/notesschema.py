from pydantic import BaseModel,Field
from typing import Optional

class BaseNotes(BaseModel):
    topic: Optional[str]=None,Field(max_length=100)
    text: Optional[str]=None,Field(min_length=20)

class CreateNotes(BaseNotes):
   pass


class PublicNotes(BaseNotes):
    id: int

    class Config:
        from_attributes = True
class UpdateNotes(BaseModel):
    topic: Optional[str] = None
    text: Optional[str] = None