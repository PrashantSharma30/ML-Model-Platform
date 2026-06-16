from sqlalchemy.orm import Session

from app.models.users import User
from app.repositories.user_repository import (
    get_user_by_email,
    get_user_by_username,
    update_user,
    delete_user,
    get_all_users,
    get_user_by_id
)
from app.schemas.user import UserUpdate
import os
import shutil

def update_current_user(
    db: Session,
    current_user: User,
    user_data: UserUpdate,
) -> User:

    # Update email
    if (
        user_data.email is not None
        and user_data.email != current_user.email
    ):
        existing_email = get_user_by_email(
            db,
            user_data.email,
        )

        if existing_email:
            raise ValueError(
                "Email already registered"
            )

        current_user.email = user_data.email

    # Update username
    if (
        user_data.username is not None
        and user_data.username != current_user.username
    ):
        existing_username = get_user_by_username(
            db,
            user_data.username,
        )

        if existing_username:
            raise ValueError(
                "Username already taken"
            )

        current_user.username = user_data.username

    return update_user(
        db,
        current_user,
    )

def delete_current_user(
    db: Session,
    current_user: User,
) -> None:

    user_directory = os.path.join(
        "uploaded_models",
        f"user_{current_user.id}",
    )

    if os.path.exists(user_directory):
        shutil.rmtree(user_directory)

    delete_user(
        db,
        current_user,
    )

def list_all_users(db: Session):
    return get_all_users(db)

def get_user_details(
    db: Session,
    user_id: int,
):
    user = get_user_by_id(db, user_id)

    if not user:
        raise ValueError("User not found")

    return user


def admin_delete_user(
    db: Session,
    user_id: int,
) -> None:

    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:
        raise ValueError("User not found")

    user_directory = os.path.join(
        "uploaded_models",
        f"user_{user.id}",
    )

    if os.path.exists(user_directory):
        shutil.rmtree(user_directory)

    delete_user(
        db,
        user,
    )

def reset_prediction_quota(
    db: Session,
    user_id: int,
) -> User:

    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:
        raise ValueError(
            "User not found"
        )

    user.prediction_quota = 15

    return update_user(
        db,
        user,
    )