from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    prediction_quota: int

    model_config = {
        "from_attributes": True
    }