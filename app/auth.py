import hashlib
import os
from dotenv import load_dotenv
from passlib.context import CryptContext


load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_signature(account_id: int, amount: float, transaction_id: str, user_id: int) -> str:
    data = f"{account_id}{amount}{transaction_id}{user_id}{os.getenv('SECRET_KEY')}"
    return hashlib.sha256(data.encode()).hexdigest()
