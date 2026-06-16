from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.users import User
from app.schemas.user import UserUpdate, UserResponse
from app.services.user_services import update_current_user,delete_current_user

from fastapi import status



router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.patch(
    "/me",
    response_model=UserResponse,
)
def update_me(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_current_user(
            db=db,
            current_user=current_user,
            user_data=user_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    

@router.delete("/me")
def delete_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_current_user(
        db=db,
        current_user=current_user,
    )

    return {
        "message": "User deleted successfully"
    }