from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.dependencies.admin import (
    get_current_admin,
)
from app.dependencies.database import get_db
from app.schemas.user import UserResponse
from app.services.user_services import (
    admin_delete_user,
    get_user_details,
    list_all_users,
    reset_prediction_quota
)

from app.schemas.model import ModelResponse

from app.services.model_service import (
    admin_delete_model,
    admin_get_model,
    list_all_models,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.get(
    "/users",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return list_all_users(db)

@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    try:
        return get_user_details(
            db,
            user_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.delete(
    "/users/{user_id}",
)
def delete_user_by_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    try:
        admin_delete_user(
            db,
            user_id,
        )

        return {
            "message":
            "User deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.get(
    "/models",
    response_model=list[ModelResponse],
)
def get_models(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return list_all_models(db)

@router.get(
    "/models/{model_id}",
    response_model=ModelResponse,
)
def get_model(
    model_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    try:
        return admin_get_model(
            db,
            model_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.delete(
    "/models/{model_id}",
)
def delete_model(
    model_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    try:
        admin_delete_model(
            db,
            model_id,
        )

        return {
            "message":
            "Model deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.patch(
    "/users/{user_id}/reset-quota",
)
def reset_quota(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    try:
        user = reset_prediction_quota(
            db,
            user_id,
        )

        return {
            "message":
                "Prediction quota reset successfully",
            "prediction_quota":
                user.prediction_quota,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )