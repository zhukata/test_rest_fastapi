from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: EmailStr
    full_name: str


class AccountResponse(BaseModel):
    id: int
    balance: float
    
    class Config:
        from_attributes = True


class PaymentResponse(BaseModel):
    id: int
    account_id: int
    amount: int
    
    class Config:
        from_attributes = True


class PaymentWebhook(BaseModel):
    account_id: int
    amount: int
    transaction_id: str
    user_id: int
    signature: str
