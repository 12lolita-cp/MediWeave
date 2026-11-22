from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PharmacyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    licensing_authority: str = Field(max_length=100)
    registration_number: str = Field(max_length=80)
    contact_email: EmailStr | None = None
    contact_phone: str | None = Field(default=None, max_length=20)


class PharmacyResponse(BaseModel):
    id: int
    name: str
    licensing_authority: str
    registration_number: str
    contact_email: EmailStr | None
    contact_phone: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)