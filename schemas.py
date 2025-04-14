from pydantic import BaseModel
from typing import Optional
from models import RoleEnum

class RoleCreate(BaseModel):
    name: RoleEnum
    description: Optional[str] = None

class RoleOut(BaseModel):
    id: int
    name: RoleEnum
    description: Optional[str]

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role_id: Optional[int] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_staff: bool
    is_active: bool
    role: Optional[RoleOut]

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str
