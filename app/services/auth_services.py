from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.users import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.schemas.auth import UserRegister


def register_user(db: Session, user_data: UserRegister) -> User:
    # Check if email already exists
    existing_email = get_user_by_email(db, user_data.email)

    if existing_email:
        raise ValueError("Email already registered")

    # Check if username already exists
    existing_username = get_user_by_username(db, user_data.username)

    if existing_username:
        raise ValueError("Username already taken")

    # Create user object
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_active=True,
        is_admin=False,
        prediction_quota=15,
    )

    return create_user(db, user)

from app.core.security import (
    create_access_token,
    verify_password,
)


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> str:
    """
    Authenticate a user and return a JWT access token.
    """

    user = get_user_by_email(db, email)

    if not user:
        raise ValueError("User does not exist")

    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid password")

    if not user.is_active:
        raise ValueError("Inactive user")

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return access_token