from typing import Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.models import User


# =========================
# Password Hashing
# =========================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# =========================
# User CRUD Operations
# =========================
def create_user(
    db: Session,
    name: str,
    email: str,
    username: str,
    password: str
) -> User:
    hashed_password = hash_password(password)

    db_user = User(
        name=name,
        email=email,
        username=username,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # REQUIRED for created_at, id, etc.

    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()
