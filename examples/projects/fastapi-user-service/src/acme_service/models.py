"""User models for FastAPI service."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserBase(BaseModel):
    """Base user model with common fields."""

    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(..., min_length=1, max_length=100, description="User full name")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    is_active: bool = Field(default=True, description="Whether user is active")


class UserCreate(UserBase):
    """User creation model."""

    password: str = Field(..., min_length=8, max_length=100, description="User password")


class UserUpdate(BaseModel):
    """User update model with optional fields."""

    email: EmailStr | None = None
    full_name: str | None = Field(None, min_length=1, max_length=100)
    role: UserRole | None = None
    is_active: bool | None = None
    password: str | None = Field(None, min_length=8, max_length=100)


class User(UserBase):
    """User response model."""

    id: UUID = Field(default_factory=uuid4, description="User unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Update timestamp")

    class Config:
        """Pydantic config."""

        from_attributes = True


class UserInDB(User):
    """User model as stored in database."""

    hashed_password: str = Field(..., description="Hashed password")
