from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, constr


class ProfileSchema(BaseModel):
    username: str
    bio: str
    follower_count: int
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class CreateUserSchema(BaseModel):
    password: constr(min_length=8)
    email: str
    
    class Config:
        orm_mode = True



class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

    class Config:
        orm_mode = True


class UserResponseSchema(ProfileSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class FilteredUserResponse(ProfileSchema):
    id: str


class TokenData(BaseModel):
    email: EmailStr | None = None