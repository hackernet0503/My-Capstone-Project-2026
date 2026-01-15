from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.models import User
from app.schemas.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------
# Password helpers
# -----------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# -----------------------------
# Get users
# -----------------------------
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# -----------------------------
# Create user
# -----------------------------
def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
