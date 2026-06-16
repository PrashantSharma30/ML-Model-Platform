from sqlalchemy.orm import Session

from app.models.ml_models import MLModel
from app.models.users import User
from app.repositories.model_repository import (
    create_model,
    delete_model,
    get_model_by_id,
    get_models_by_user,
    update_model,
    get_all_models,
    update_model_file_path
)
from app.schemas.model import (
    ModelCreate,
    ModelUpdate,
    PredictionRequest
)

import os
import shutil
import joblib

from fastapi import UploadFile

def register_model(
    db: Session,
    current_user: User,
    model_data: ModelCreate,
) -> MLModel:

    model = MLModel(
        name=model_data.name,
        description=model_data.description,
        version=model_data.version,
        framework=model_data.framework,
        owner_id=current_user.id,
    )

    return create_model(db, model)

def list_user_models(
    db: Session,
    current_user: User,
) -> list[MLModel]:

    return get_models_by_user(
        db,
        current_user.id,
    )

def get_user_model(
    db: Session,
    current_user: User,
    model_id: int,
) -> MLModel:

    model = get_model_by_id(
        db,
        model_id,
    )

    if not model:
        raise ValueError("Model not found")

    if model.owner_id != current_user.id:
        raise ValueError("Access denied")

    return model

def update_user_model(
    db: Session,
    current_user: User,
    model_id: int,
    model_data: ModelUpdate,
) -> MLModel:

    model = get_user_model(
        db,
        current_user,
        model_id,
    )

    if model_data.name is not None:
        model.name = model_data.name

    if model_data.description is not None:
        model.description = model_data.description

    if model_data.version is not None:
        model.version = model_data.version

    if model_data.framework is not None:
        model.framework = model_data.framework

    return update_model(
        db,
        model,
    )

def delete_user_model(
    db: Session,
    current_user: User,
    model_id: int,
) -> None:

    model = get_user_model(
        db,
        current_user,
        model_id,
    )

    if (
        model.file_path
        and os.path.exists(model.file_path)
    ):
        os.remove(model.file_path)

    delete_model(
        db,
        model,
    )

def list_all_models(
    db: Session,
) -> list[MLModel]:

    return get_all_models(db)

def admin_get_model(
    db: Session,
    model_id: int,
) -> MLModel:

    model = get_model_by_id(
        db,
        model_id,
    )

    if not model:
        raise ValueError(
            "Model not found"
        )

    return model

def admin_delete_model(
    db: Session,
    model_id: int,
) -> None:

    model = get_model_by_id(
        db,
        model_id,
    )

    if not model:
        raise ValueError("Model not found")

    if (
        model.file_path
        and os.path.exists(model.file_path)
    ):
        os.remove(model.file_path)

    delete_model(
        db,
        model,
    )

def upload_model_file(
    db: Session,
    current_user: User,
    model_id: int,
    file: UploadFile,
) -> MLModel:

    model = get_user_model(
        db,
        current_user,
        model_id,
    )

    allowed_extensions = {
        ".pkl",
        ".joblib",
    }

    _, extension = os.path.splitext(
        file.filename
    )

    extension = extension.lower()

    if extension not in allowed_extensions:
        raise ValueError(
            "Only .pkl and .joblib files are allowed"
        )

    user_directory = os.path.join(
        "uploaded_models",
        f"user_{current_user.id}",
    )

    os.makedirs(
        user_directory,
        exist_ok=True,
    )

    file_name = (
        f"model_{model.id}{extension}"
    )

    file_path = os.path.join(
        user_directory,
        file_name,
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return update_model_file_path(
        db,
        model,
        file_path,
    )

def predict_with_model(
    db: Session,
    current_user: User,
    model_id: int,
    prediction_data: PredictionRequest,
):
    if current_user.prediction_quota <= 0:
        raise ValueError(
            "Prediction quota exceeded"
        )
    model_record = get_user_model(
        db,
        current_user,
        model_id,
    )

    if not model_record.file_path:
        raise ValueError(
            "No model file uploaded"
        )

    loaded_model = joblib.load(
        model_record.file_path
    )

    prediction = loaded_model.predict(
        [prediction_data.features]
    )
    current_user.prediction_quota -= 1

    db.commit()
    db.refresh(current_user)

    return prediction.tolist()