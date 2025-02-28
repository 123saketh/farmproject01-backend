from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id:Optional[str]= None
    firstName: str
    lastName: str
    email: str
    jobTitle: str
    gender: str