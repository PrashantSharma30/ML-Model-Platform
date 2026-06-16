from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.auth import UserRegister
from app.services.auth_services import register_user
from app.schemas.auth import Token, UserLogin
from app.services.auth_services import authenticate_user

from app.dependencies.auth import get_current_user
from app.models.users import User

from fastapi import BackgroundTasks
from app.services.email_services import send_welcome_email

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        user = register_user(db, user_data)
        background_tasks.add_task(
            send_welcome_email,
            recipient_email=user.email,
            username=user.username,
        )
        return {
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "is_admin": user.is_admin,
                "prediction_quota": user.prediction_quota,
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

@router.post(
    "/login",
    response_model=Token,
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        access_token = authenticate_user(
            db=db,
            email=credentials.email,
            password=credentials.password,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    
    
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_admin": current_user.is_admin,
        "prediction_quota": current_user.prediction_quota,
    }

