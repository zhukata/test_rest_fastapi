from pydantic import BaseModel, Field, EmailStr


class UserСreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class User(UserСreate):
    id: int
