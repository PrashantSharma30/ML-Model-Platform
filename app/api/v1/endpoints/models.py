from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from fastapi import File, UploadFile
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.users import User
from app.schemas.model import (
    ModelCreate,
    ModelResponse,
    ModelUpdate,
    PredictionRequest,
    PredictionResponse,
)
from app.services.model_service import (
    delete_user_model,
    get_user_model,
    list_user_models,
    register_model,
    update_user_model,
    upload_model_file,
    predict_with_model
)

router = APIRouter(
    prefix="/models",
    tags=["Models"],
)

@router.post(
    "",
    response_model=ModelResponse,
)
def create_model(
    model_data: ModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return register_model(
        db=db,
        current_user=current_user,
        model_data=model_data,
    )

@router.get(
    "",
    response_model=list[ModelResponse],
)
def get_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_models(
        db=db,
        current_user=current_user,
    )

@router.get(
    "/{model_id}",
    response_model=ModelResponse,
)
def get_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_user_model(
            db=db,
            current_user=current_user,
            model_id=model_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.patch(
    "/{model_id}",
    response_model=ModelResponse,
)
def patch_model(
    model_id: int,
    model_data: ModelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_user_model(
            db=db,
            current_user=current_user,
            model_id=model_id,
            model_data=model_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.delete(
    "/{model_id}",
)
def remove_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_user_model(
            db=db,
            current_user=current_user,
            model_id=model_id,
        )

        return {
            "message": "Model deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.post(
    "/{model_id}/upload",
    response_model=ModelResponse,
)
def upload_file(
    model_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return upload_model_file(
            db=db,
            current_user=current_user,
            model_id=model_id,
            file=file,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
@router.post(
    "/{model_id}/predict",
    response_model=PredictionResponse,
)
def predict(
    model_id: int,
    prediction_data: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        prediction = predict_with_model(
            db=db,
            current_user=current_user,
            model_id=model_id,
            prediction_data=prediction_data,
        )

        return {
            "prediction": prediction
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )