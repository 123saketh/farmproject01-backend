from typing import Optional
from pydantic import BaseModel


class UpdateUser(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    jobTitle: Optional[str] = None
    gender: Optional[str] = None