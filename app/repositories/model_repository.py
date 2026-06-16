from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ml_models import MLModel

def create_model(
    db: Session,
    model: MLModel,
) -> MLModel:
    db.add(model)
    db.commit()
    db.refresh(model)

    return model

def get_models_by_user(
    db: Session,
    owner_id: int,
) -> list[MLModel]:

    stmt = (
        select(MLModel)
        .where(MLModel.owner_id == owner_id)
    )

    return list(db.scalars(stmt).all())

def get_model_by_id(
    db: Session,
    model_id: int,
) -> MLModel | None:

    stmt = (
        select(MLModel)
        .where(MLModel.id == model_id)
    )

    return db.scalar(stmt)

def update_model(
    db: Session,
    model: MLModel,
) -> MLModel:

    db.commit()
    db.refresh(model)

    return model

def delete_model(
    db: Session,
    model: MLModel,
) -> None:

    db.delete(model)
    db.commit()

def get_all_models(
    db: Session,
) -> list[MLModel]:

    stmt = select(MLModel)

    return list(db.scalars(stmt).all())

def update_model_file_path(
    db: Session,
    model: MLModel,
    file_path: str,
) -> MLModel:

    model.file_path = file_path

    db.commit()
    db.refresh(model)

    return model