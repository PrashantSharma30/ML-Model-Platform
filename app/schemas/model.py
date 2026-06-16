from datetime import datetime

from pydantic import BaseModel


class ModelCreate(BaseModel):
    name: str
    description: str | None = None
    version: str = "1.0"
    framework: str


class ModelUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    version: str | None = None
    framework: str | None = None


class ModelResponse(BaseModel):
    id: int
    name: str
    description: str | None
    version: str
    framework: str
    file_path: str | None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class PredictionRequest(BaseModel):
    features: list[float]


class PredictionResponse(BaseModel):
    prediction: list