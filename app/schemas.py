from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, model_validator


class Status(str, Enum):
    saved = "saved"
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"


class ApplicationCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    company: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=200)
    status: Status = Status.saved
    applied_on: date | None = None
    url: str | None = None
    notes: str | None = None


class ApplicationUpdate(BaseModel):
    @model_validator(mode="after")
    def no_null_required_fields(self):
        for name in ("company", "role", "status"):
            if name in self.model_fields_set and getattr(self, name) is None:
                raise ValueError(f"{name} cannot be null")
        return self
    model_config = ConfigDict(use_enum_values=True)

    company: str | None = Field(default=None, min_length=1, max_length=200)
    role: str | None = Field(default=None, min_length=1, max_length=200)
    status: Status | None = None
    applied_on: date | None = None
    url: str | None = None
    notes: str | None = None


class ApplicationOut(ApplicationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int